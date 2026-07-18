from django.db.models import Q
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
from restapi.serializers.generic import (
    BaseExcelImportSerializer,
    build_bulk_lookup_map,
    parse_semicolon_string,
)


class PlantVarietyListSerializer(sr.ListSerializer):
    def to_internal_value(self, data):
        self.context["variety_map"] = build_bulk_lookup_map(PlantVariety.objects.all(), ["name", "species"], data)
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


class ProtectionListSerializer(sr.ListSerializer):
    default_error_messages = {
        "duplicates": "Duplicate matches for {dupes}",
    }

    def merge_entities(self, data):
        # Entities come from `applicants` and `maintainers` fields, so
        # we build the mapping once by merging column values. Also,
        # values are expected as semicolon-separated, hence
        # `parse_semicolon_string`.
        entities = []
        for row in data:
            for column in ["applicants", "maintainers"]:
                column_value = row.get(column, None)
                if column_value and isinstance(column_value, str):
                    entities.extend([{"name": value} for value in parse_semicolon_string(column_value)])
        return entities

    def to_internal_value(self, data):
        self.context["entity_map"] = build_bulk_lookup_map(
            Entity.objects.all(),
            ["name"],
            self.merge_entities(data),
        )
        self.context["variety_map"] = build_bulk_lookup_map(
            PlantVariety.objects.all(),
            ["name", "species_id"],
            data,
        )
        self.context["protection_type_map"] = build_bulk_lookup_map(
            ProtectionType.objects.all(),
            {"type": "code"},
            data,
        )
        return super().to_internal_value(data)

    def create(self, validated_data):
        lookup_values = {
            (
                item["type"].pk,
                item["variety"].pk,
                item["country"],
            )
            for item in validated_data
            if item.get("type") and item.get("variety") and item.get("country")
        }

        query = Q()
        for type_id, variety_id, country in lookup_values:
            query |= Q(
                type_id=type_id,
                variety_id=variety_id,
                country=country,
            )

        protection_keys = set()

        if query:
            protection_keys = set(Protection.objects.filter(query).values_list("type_id", "variety_id", "country"))

        results = []

        for item in validated_data:
            ptype = item.get("type")
            variety = item.get("variety")
            country = item.get("country")

            key = (
                ptype.pk if ptype else None,
                variety.pk if variety else None,
                country,
            )

            if key in protection_keys:
                results.append((None, [], []))
                continue

            applicants = item.pop("applicants", [])
            maintainers = item.pop("maintainers", [])

            protection = Protection(**item)

            results.append((protection, applicants, maintainers))

            # Prevent duplicate creation within same import payload.
            protection_keys.add(key)

        return results


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
        applicants = validated_data.pop("applicants", [])
        maintainers = validated_data.pop("maintainers", [])
        return Protection(**validated_data), applicants, maintainers


class ProtectionExcelImportSerializer(BaseExcelImportSerializer):
    row_serializer = ProtectionRowSerializer


class EntityListSerializer(sr.ListSerializer):
    def to_internal_value(self, data):
        self.context["entity_map"] = build_bulk_lookup_map(
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
