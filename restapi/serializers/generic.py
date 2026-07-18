from collections.abc import Mapping, Sequence
from typing import Any

import pandas as pd
from django.core.exceptions import ValidationError
from django.db.models import Q
from rest_framework import serializers as sr


def parse_semicolon_string(data: str):
    return [value for item in data.split(";") if (value := item.strip())]


def build_bulk_lookup_map(
    queryset,
    lookup_fields: Sequence[str] | Mapping[str, str],
    data: list[dict[str, Any]],
) -> dict[tuple[Any, ...], Any]:
    if isinstance(lookup_fields, Mapping):
        input_columns = tuple(lookup_fields.keys())
        model_fields = tuple(lookup_fields.values())
    else:
        input_columns = tuple(lookup_fields)
        model_fields = tuple(lookup_fields)

    lookup_values: set[tuple[Any, ...]] = set()

    for row in data:
        row_lookup = tuple(row.get(column) for column in input_columns)
        if all(row_lookup):
            lookup_values.add(row_lookup)

    if not lookup_values:
        return {}

    query = Q()
    for row_lookup in lookup_values:
        query |= Q(*zip(model_fields, row_lookup, strict=True))

    mapping: dict[tuple[Any, ...], Any] = {}
    for obj in queryset.filter(query):
        lookup_key = tuple(getattr(obj, field) for field in model_fields)
        mapping[lookup_key] = obj

    return mapping


class BulkListSerializer(sr.ListSerializer):
    def create(self, validated_data):
        model_class = self.child.Meta.model
        return model_class.objects.bulk_create([model_class(**item) for item in validated_data])


class BulkModelSerializer(sr.ModelSerializer):
    class Meta:
        list_serializer_class = BulkListSerializer


class BaseExcelImportSerializer(sr.Serializer):
    file = sr.FileField(label="Excel file (.xlsx)")
    validate_only = sr.BooleanField(default=False, label="Validate only")

    row_serializer: type[sr.Serializer]

    @staticmethod
    def catch_row_serializer_errors(exc):
        MAX_ERRORS = 100
        errors = []
        error_count = len([error for error in exc.detail if error])
        if error_count > MAX_ERRORS:
            errors.append(
                {"non_field_errors": f"There are {error_count} errors; only the first {MAX_ERRORS} are shown."}
            )
        appended = 0
        for index, error in enumerate(exc.detail, start=2):
            if error:
                errors.append({"row": index, "error": error})
                appended += 1
            if appended >= MAX_ERRORS:
                break
        return errors

    def validate_file(self, value):
        try:
            pd.read_excel(value, nrows=0)
        except Exception as err:
            raise ValidationError("The uploaded file is not a valid Excel file.") from err
        return value

    def validate(self, attrs):
        assert self.row_serializer, "row_serializer must be set on the subclass."

        try:
            df = pd.read_excel(attrs["file"], keep_default_na=True)
        except Exception as e:
            raise sr.ValidationError({"file": f"Error reading Excel: {e}"}) from e

        rows = []

        for row in df.to_dict(orient="records"):
            rows.append({k: v for k, v in row.items() if pd.notna(v) and v != ""})

        attrs["_rows"] = rows
        return attrs

    def create(self, validated_data):
        rows = validated_data.pop("_rows", [])
        row_serializer = self.row_serializer(data=rows, many=True)
        row_serializer.is_valid(raise_exception=True)
        if validated_data.get("validate_only"):
            return []
        objs = row_serializer.save()
        return objs


class ExcelImportResponseSerializer(sr.Serializer):
    imported_rows = sr.IntegerField()
