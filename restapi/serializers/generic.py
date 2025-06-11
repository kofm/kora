import pandas as pd
from django.core.exceptions import ValidationError
from django.db.models import Q
from rest_framework import serializers as sr


class BulkListSerializer(sr.ListSerializer):
    def create(self, validated_data):
        model_class = self.child.Meta.model
        return model_class.objects.bulk_create([model_class(**item) for item in validated_data])


class BulkModelSerializer(sr.ModelSerializer):
    class Meta:
        list_serializer_class = BulkListSerializer


class ModelInBulkMixin:
    @staticmethod
    def to_mapping(queryset, lookup_fields: list | dict, data: list[dict]) -> dict:
        uniq = set()
        if isinstance(lookup_fields, list):
            cols = lookup_fields
            lf = lookup_fields
        elif isinstance(lookup_fields, dict):
            cols = lookup_fields.keys()
            lf = lookup_fields.values()
        for row in data:
            vals = tuple(row.get(k, None) for k in cols)
            if all(vals):
                uniq.add(vals)

        query = Q()
        for key in uniq:
            query |= Q(*zip(lf, key, strict=True))
        qs = queryset.filter(query)

        mapping = {}
        for obj in qs:
            k = tuple(getattr(obj, x) for x in lf)
            mapping.update({k: obj})

        return mapping


class BaseExcelImportSerializer(sr.Serializer):
    file = sr.FileField(label="Excel file (.xlsx)")
    validate_only = sr.BooleanField(default=False, label="Validate only")

    row_serializer: type[sr.Serializer]

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
        objs = row_serializer.save()
        return objs
