import pandas as pd
from django.core.exceptions import ValidationError
from django.db.models import Count, Q
from rest_framework import serializers as sr
from rest_framework.fields import SkipField

from register.models import Entity, PlantSpecies, PlantVariety, PlantVarietyName, Protection
from restapi.fields import ChoiceColumnField, CountryColumnField, DateColumnField


class BaseExcelImport(sr.Serializer):
    file = sr.FileField(required=True)
    validate_only = sr.BooleanField(default=False)

    row_serializer = None

    def validate_file(self, value):
        try:
            pd.read_excel(value, nrows=1)
        except Exception as e:
            raise sr.ValidationError(f"Cannot open Excel file: {e}") from e
        return value

    def validate(self, attrs):
        assert self.row_serializer, "row_serializer must be set on the subclass."

        try:
            df = pd.read_excel(attrs["file"], keep_default_na=False)
        except Exception as e:
            raise sr.ValidationError({"file": f"Error reading Excel: {e}"}) from e

        rows = df.to_dict(orient="records")

        RowSerializer = self.row_serializer
        row_serializer = RowSerializer()

        column_fields = {
            fname: fobj for fname, fobj in row_serializer.fields.items() if isinstance(fobj, BaseColumnField)
        }

        maps = {}
        for field_name, field in column_fields.items():
            unique_values = field.unique_values(rows)
            mapping = field.bulk_resolve(unique_values)
            maps[field_name] = mapping

        attrs["_rows"] = rows
        attrs["_column_maps"] = maps
        return attrs

    def create(self, validated):
        rows, maps = validated.pop("_rows"), validated.pop("_column_maps")

        valid, errors = [], []
        for index, row in enumerate(rows, start=1):
            row = {k: v for k, v in row.items() if pd.notna(v) and v != ""}
            row_serializer = self.row_serializer(data=row, context={"_column_maps": maps})
            if row_serializer.is_valid():
                valid.append(row_serializer)
            else:
                errors.append({"row": index, "errors": row_serializer.errors})

        if errors:
            raise sr.ValidationError(errors)

        if not self.validated_data["validate_only"]:
            for s in valid:
                s.save()

        return {"imported": len(valid)}


class BaseColumnField(sr.Field):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._mapping = {}

    @staticmethod
    def _is_blank(value):
        """True for ``None`` or an empty / whitespace‑only string."""
        return value is None or (isinstance(value, str) and value.strip() == "")

    def unique_values(self, rows):
        raise NotImplementedError

    def bulk_resolve(self, distinct_values):
        raise NotImplementedError

    def to_internal_value(self, raw):
        if raw in (None, ""):
            return None
        try:
            return self.context["_column_maps"][self.field_name][raw]
        except KeyError as e:
            raise sr.ValidationError(f"{raw!r} not recognised") from e


class FKColumn(BaseColumnField):
    def __init__(self, *, model, field: str, column: str, create_missing=False, **kwargs):
        super().__init__(**kwargs)
        self.model = model
        self.field = field
        self.column = column
        self.create_missing = create_missing

    def _inspect_row(self, data):
        value = data.get(self.column)

        if self._is_blank(value):
            if self.required:
                raise sr.ValidationError(f"{self.column} is required")
            return None

        return value

    def unique_values(self, rows):
        uniq = set()
        for index, row in enumerate(rows):
            try:
                value = self._inspect_row(row)
            except sr.ValidationError as err:
                raise sr.ValidationError({"non_field_errors": f"Row {index}: {err.args[0]}"}) from err
            if value not in (None, ""):
                uniq.add(value)
        return uniq

    def bulk_resolve(self, unique_values):
        existing = self.model.objects.filter(**{f"{self.field}__in": unique_values})
        mapping = {getattr(obj, self.field): obj for obj in existing}

        missing = unique_values - set(mapping.keys())
        if missing and not self.create_missing:
            raise sr.ValidationError({self.column: f"Missing {self.model.__name__} objects for {missing!r}"})

        if missing and self.create_missing:
            objs = [self.model(**{self.field: val}) for val in missing]
            created = self.model.objects.bulk_create(objs)
            mapping.update({getattr(obj, self.field): obj for obj in created})

        self._mapping = mapping
        return self._mapping


class QueryColumn(BaseColumnField):
    def __init__(self, *, model, col_map, create_missing=False, **kwargs):
        super().__init__(**kwargs)
        self.model = model
        self.col_map: dict = col_map
        self.create_missing = create_missing

    def _inspect_row(self, data):
        cols = self.col_map.keys()
        values = tuple(data.get(col) for col in cols)
        blanks = [self._is_blank(v) for v in values]

        if all(blanks):
            if self.required:
                raise sr.ValidationError(f"{', '.join(cols)} are required but missing")
            return None

        if any(blanks) and self.required:
            raise sr.ValidationError(f"{', '.join(cols)} must all be complete pairs")

        if any(blanks) and not self.required:
            return None

        return values

    def unique_values(self, rows: list[dict]):
        """Collect the set of composite‑key tuples that actually need look‑up."""
        uniques = set()
        for index, row in enumerate(rows, start=1):
            try:
                values = self._inspect_row(row)
            except sr.ValidationError as err:
                raise sr.ValidationError({"non_field_errors": f"Row {index}: {err.args[0]}"}) from err
            if values is not None:
                uniques.add(values)
        return uniques

    def bulk_resolve(self, unique_values):
        query = Q()
        for tup in unique_values:
            filters = dict(zip(self.col_map.values(), tup, strict=True))
            query |= Q(**filters)

        queryset = self.model.objects.filter(query)
        duplicates = queryset.values(*self.col_map.values()).annotate(count=Count("pk")).filter(count__gt=1)

        if duplicates.exists():
            raise ValidationError(
                "Some of {', '.join(self.col_map.keys())} values match more than one record in the database: "
                f"{list(duplicates)}"
            )

        existing_objs = list(queryset)
        existing = {tuple(getattr(obj, field) for field in self.col_map.values()) for obj in existing_objs}
        missing = unique_values - existing
        if missing:
            if self.create_missing:
                objs = [
                    self.model(**dict(zip(self.col_map.values(), prov, strict=True)))
                    for prov in unique_values
                    if prov not in existing
                ]
                existing_objs += self.model.objects.bulk_create(objs)
            else:
                raise sr.ValidationError(
                    f"Some of the {', '.join(self.col_map.keys())} values don't match any record in the database: {missing}"
                )
        mapping = {tuple(getattr(obj, field) for field in self.col_map.values()): obj for obj in existing_objs}
        return mapping

    def get_value(self, data):
        values = self._inspect_row(data)
        if values is None:
            raise SkipField
        # We don’t care about the cell contents here; `to_internal_value`
        # will pull the actual values from `self.parent.initial_data`.
        return object()  # any sentinel value is fine

    def to_internal_value(self, _sentinel):
        if self.parent is None:  # safety net
            raise sr.ValidationError("No parent serializer set")

        # Build key in the same order declared in `col_map`
        key = tuple(self.parent.initial_data[col] for col in self.col_map)

        try:
            return self.context["_column_maps"][self.field_name][key]
        except KeyError as e:
            raise sr.ValidationError(f"{key!r} not recognised") from e


class ManyToManyColumn(BaseColumnField):
    def __init__(self, *, model, column: str, field: str, create_missing=False, **kwargs):
        super().__init__(**kwargs)
        self.model = model
        self.column = column
        self.field = field
        self.create_missing = create_missing

    def unique_values(self, rows):
        values = set()
        for row in rows:
            raw = row.get(self.column, "") or ""
            for value in raw.split(";"):
                value = value.strip()
                if value:
                    values.add(value)
        return values

    def bulk_resolve(self, unique_values):
        queryset = self.model.objects.filter(**{f"{self.field}__in": unique_values})
        existing = list(queryset)
        existing_set = {getattr(obj, self.field) for obj in existing}

        missing = unique_values - existing_set

        if missing and not self.create_missing:
            raise sr.ValidationError({self.column: f"Missing {self.model.__name__} for {missing!r}"})

        if missing and self.create_missing:
            new_objs = [self.model(**{self.field: value}) for value in missing]
            existing += self.model.objects.bulk_create(new_objs)

        self._mapping = {getattr(obj, self.field): obj for obj in existing}
        return self._mapping

    def to_internal_value(self, raw):
        if raw in (None, "") or pd.isna(raw):
            return []
        value = []
        for val in raw.split(";"):
            val = val.strip()
            if not val:
                continue
            try:
                obj = self.context["_column_maps"][self.field_name][val]
            except KeyError as e:
                raise sr.ValidationError(f"{raw!r} not recognised") from e
            value.append(obj)
        return value


class PlantVarietyImportRowSerializer(sr.Serializer):
    name = sr.CharField(required=True)
    species = FKColumn(
        model=PlantSpecies,
        field="common_name",
        column="species",
        create_missing=True,
        required=True,
    )

    def create(self, validated_data):
        obj = PlantVariety.objects.create(**validated_data)
        return obj


class PlantVarietyImportSerializer(BaseExcelImport):
    row_serializer = PlantVarietyImportRowSerializer


class PlantVarietyQueryColumn(QueryColumn):
    def __init__(self, *, col_map, create_missing=False, **kwargs):
        model = PlantVariety
        super().__init__(model=model, col_map=col_map, create_missing=create_missing, **kwargs)

    def bulk_resolve(self, unique_values):
        query = Q()
        for tup in unique_values:
            filters = dict(zip(self.col_map.values(), tup, strict=True))
            query |= Q(**filters)

        queryset = self.model.objects.filter(query)
        duplicates = queryset.values(*self.col_map.values()).annotate(count=Count("pk")).filter(count__gt=1)

        if duplicates.exists():
            raise ValidationError(
                f"Some of {', '.join(self.col_map.keys())} values match more than one record in the database: "
                f"{list(duplicates)}"
            )

        existing_objs = list(queryset)
        existing = {tuple(getattr(obj, field) for field in self.col_map.values()) for obj in existing_objs}
        missing = unique_values - existing
        if missing:
            if self.create_missing:
                objs = [
                    self.model(**dict(zip(self.col_map.values(), prov, strict=True)))
                    for prov in unique_values
                    if prov not in existing
                ]
                created = self.model.objects.bulk_create(objs)
                PlantVarietyName.objects.bulk_create([PlantVarietyName(name=obj.name, variety=obj) for obj in created])
                existing_objs += created
            else:
                raise sr.ValidationError(
                    f"Some of the {', '.join(self.col_map.keys())} values don't match any record in the database: {missing}"
                )
        mapping = {tuple(getattr(obj, field) for field in self.col_map.values()): obj for obj in existing_objs}
        return mapping


class ProtectionRowSerializer(sr.Serializer):
    type = ChoiceColumnField(choices=["CAT", "NLI", "PBR"])
    status = ChoiceColumnField(choices=["G", "T", "S", "W"], required=False)
    variety = PlantVarietyQueryColumn(
        col_map={"variety_name": "name", "species_id": "species_id"},
        create_missing=True,
    )
    applicants = ManyToManyColumn(model=Entity, column="applicants", field="name", create_missing=True, required=False)
    maintainers = ManyToManyColumn(
        model=Entity, column="maintainers", field="name", create_missing=True, required=False
    )
    country = CountryColumnField(required=False)
    date_start = DateColumnField(required=False)
    date_end = DateColumnField(required=False)
    reference = sr.CharField(required=False)
    note = sr.CharField(required=False)

    def create(self, validated_data):
        applicants = validated_data.pop("applicants", [])
        maintainers = validated_data.pop("maintainers", [])
        obj = Protection.objects.create(**validated_data)
        obj.applicants.set(applicants)
        obj.maintainers.set(maintainers)
        return obj


class ProtectionImportSerializer(BaseExcelImport):
    row_serializer = ProtectionRowSerializer
