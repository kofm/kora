from django_countries.serializer_fields import CountryField
from rest_framework import serializers as sr

from register.models import (
    ENTITY_TYPE_CHOICES,
    PROTECTION_STATUS_CHOICES,
    Entity,
    PlantSpecies,
    PlantVariety,
    Protection,
    ProtectionType,
)
from restapi.fields import CSV2ListQueryField, ExcelSafeDateField, MappedPrimaryKeyRelatedField, QueryField
from restapi.serializers.generic import BaseExcelImportSerializer, ModelInBulkMixin, parse_semicolon_string


class PlantVarietyListSerializer(ModelInBulkMixin, sr.ListSerializer):
    def to_internal_value(self, data):
        self.context["variety_map"] = self.to_mapping(PlantVariety.objects.all(), ["name", "species"], data)
        self.context["species_map"] = PlantSpecies.objects.in_bulk()
        return super().to_internal_value(data)


class PlantVarietyImportRowSerializer(sr.Serializer):
    name = sr.CharField(required=True)
    species_id = MappedPrimaryKeyRelatedField(mapping_key="species_map", required=True, source="species")

    class Meta:
        list_serializer_class = PlantVarietyListSerializer

    def create(self, validated_data):
        name = validated_data.get("name")
        species = validated_data.get("species")
        if (name, species) not in self.context["variety_map"]:
            return PlantVariety(**validated_data)
        return None


class PlantVarietyImportSerializer(BaseExcelImportSerializer):
    row_serializer = PlantVarietyImportRowSerializer


class ProtectionListSerializer(ModelInBulkMixin, sr.ListSerializer):
    default_error_messages = {
        "duplicates": "Duplicate matches for {dupes}",
    }

    def to_internal_value(self, data):
        entities = []
        for row in data:
            m = row.get("applicants", None)
            if m and isinstance(m, str):
                vals = m.split(";")
                for val in vals:
                    entities.append({"name": val.strip()})
            m = row.get("maintainers", None)
            if m and isinstance(m, str):
                vals = m.split(";")
                for val in vals:
                    entities.append({"name": val.strip()})
        self.context["entity_map"] = self.to_mapping(Entity.objects.all(), ["name"], entities)
        self.context["protection_map"] = self.to_mapping(
            Protection.objects.select_related("variety").prefetch_related("applicants", "maintainers"),
            ["type", "variety", "country"],
            data,
        )
        self.context["variety_map"] = self.to_mapping(PlantVariety.objects.all(), ["name", "species_id"], data)
        self.context["protection_type_map"] = self.to_mapping(ProtectionType.objects.all(), ["code"], data)
        return super().to_internal_value(data)


class ProtectionRowSerializer(sr.Serializer):
    variety = QueryField(
        mapping_key="variety_map",
        column_mapping={"name": "name", "species_id": "species_id"},
        required=True,
    )
    type = QueryField(mapping_key="protection_type_map", column_mapping={"type": "code"}, required=True)
    reference = sr.CharField(required=False, allow_blank=True)
    status = sr.ChoiceField(choices=PROTECTION_STATUS_CHOICES, required=False)
    country = CountryField(required=False)
    date_start = ExcelSafeDateField(required=False, allow_null=True)
    date_end = ExcelSafeDateField(required=False, allow_null=True)
    applicants = CSV2ListQueryField(mapping_key="entity_map", column_mapping={"applicants": "name"}, required=False)
    maintainers = CSV2ListQueryField(mapping_key="entity_map", column_mapping={"maintainers": "name"}, required=False)
    note = sr.CharField(required=False, allow_blank=True)

    class Meta:
        list_serializer_class = ProtectionListSerializer

    def create(self, validated_data):
        ptype = validated_data.get("type")
        variety = validated_data.get("variety")
        country = validated_data.get("country")
        if (ptype, variety, country) in self.context["protection_map"]:
            return None, [], []
        applicants = validated_data.pop("applicants", [])
        maintainers = validated_data.pop("maintainers", [])
        return Protection(**validated_data), applicants, maintainers


class ProtectionExcelImportSerializer(BaseExcelImportSerializer):
    row_serializer = ProtectionRowSerializer


class EntityListSerializer(ModelInBulkMixin, sr.ListSerializer):
    def to_internal_value(self, data):
        self.context["entity_map"] = self.to_mapping(
            queryset=Entity.objects.all(),
            lookup_fields=["name"],
            data=data,
        )
        return super().to_internal_value(data)


class EntityImportRowSerializer(sr.Serializer):
    name = sr.CharField(required=True)
    type = sr.ChoiceField(choices=ENTITY_TYPE_CHOICES, required=False)
    country = CountryField(required=False)
    contact = sr.CharField(max_length=500, required=False)
    email = sr.EmailField(required=False)

    class Meta:
        list_serializer_class = EntityListSerializer

    def create(self, validated_data):
        name = validated_data.get("name")
        if (name,) not in self.context["entity_map"]:
            return Entity(**validated_data)


class EntityImportSerializer(BaseExcelImportSerializer):
    row_serializer = EntityImportRowSerializer
