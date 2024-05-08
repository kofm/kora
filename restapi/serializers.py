import math

from rest_framework import serializers
from django_countries.serializers import CountryFieldMixin
from collect.models import CartItem, SeedSample, StoragePosition, Storage
from describe.models import (
    DescriptionsUserList,
    DescriptionsUserListElement,
    Description,
    Expression,
    Protocol,
    Trait,
    State,
)

from parameters.models import VarietalParameter
from register.models import Entity, PlantSpecies, PlantVariety, PlantVarietyName, Protection


class PlantSpeciesSerializer(serializers.ModelSerializer):
    class Meta:
        model = PlantSpecies
        fields = ["pk", "common_name", "latin_name", "plant_type"]


class PlantVarietyNameSerializer(serializers.ModelSerializer):
    class Meta:
        model = PlantVarietyName
        fields = ["name"]


class PlantVarietySerializer(serializers.ModelSerializer):
    names = PlantVarietyNameSerializer(many=True, read_only=True)

    class Meta:
        model = PlantVariety
        fields = ["pk", "name", "species", "breeder", "names"]


class EntitySerializer(CountryFieldMixin, serializers.ModelSerializer):
    class Meta:
        model = Entity
        fields = ["pk", "name", "type", "country", "contact", "email"]


class ProtectionSerializer(CountryFieldMixin, serializers.ModelSerializer):
    class Meta:
        model = Protection
        fields = [
            "pk",
            "type",
            "status",
            "country",
            "variety",
            "reference",
            "applicants",
            "maintainers",
            "date_start",
            "date_end",
            "note",
        ]


class ProtocolSerializer(serializers.ModelSerializer):
    class Meta:
        model = Protocol
        fields = ("pk", "name", "plantspecies", "url_ref")


class StateSerializer(serializers.ModelSerializer):
    class Meta:
        model = State
        fields = ("pk", "numeric_id", "description", "trait")


class TraitSerializer(serializers.ModelSerializer):
    class Meta:
        model = Trait
        fields = ("pk", "numeric_id", "description", "protocol")


class DescriptionExpressionSerializer(serializers.ModelSerializer):
    trait = serializers.StringRelatedField(many=False, source="state.trait", read_only=True)
    state_description = serializers.StringRelatedField(many=False, source="state", read_only=True)

    class Meta:
        model = Expression
        fields = ("state", "trait", "state_description", "note")


class DescriptionSerializer(serializers.ModelSerializer):
    variety_name = serializers.CharField(source="variety.name", read_only=True)
    species = serializers.StringRelatedField(source="variety.species.latin_name", read_only=True)
    protocol_name = serializers.StringRelatedField(source="protocol.name", read_only=True)
    expressions = DescriptionExpressionSerializer(many=True, read_only=True)

    class Meta:
        model = Description
        fields = ("pk", "name", "variety", "variety_name", "species", "protocol", "protocol_name", "expressions")


class ExpressionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Expression
        fields = ("description", "state", "note")


class VarietalParameterSerializer(serializers.ModelSerializer):
    variety_name = serializers.StringRelatedField(many=False, source="variety", read_only=True)
    parameter_code = serializers.StringRelatedField(many=False, source="parameter", read_only=True)

    class Meta:
        model = VarietalParameter
        fields = "__all__"


class StorageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Storage
        fields = ("pk", "name", "order")


class StoragePositionSerializer(serializers.ModelSerializer):
    class Meta:
        model = StoragePosition
        fields = ("pk", "name", "storage")

    def get_storage_verbose_name(self, obj):
        return str(obj)


class SeedSampleSerializer(serializers.ModelSerializer):
    germinability = serializers.SerializerMethodField(read_only=True)
    weight = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = SeedSample
        fields = (
            "pk",
            "sample_id",
            "variety",
            "notes",
            "growing_season",
            "position",
            "germinability",
            "weight",
        )

    def get_germinability(self, obj):
        germinability = obj.germinability
        return 0.0 if germinability is None or math.isnan(germinability) else germinability

    def get_weight(self, obj):
        weight = obj.weight
        return 0.0 if weight is None or math.isnan(weight) else weight


class CartSerializer(serializers.ModelSerializer):
    variety_name = serializers.CharField(source="sample.variety.name", read_only=True)
    variety_id = serializers.IntegerField(source="sample.variety.pk", read_only=True)
    storage = serializers.CharField(source="sample.position")

    class Meta:
        model = CartItem
        fields = ("variety_name", "variety_id", "sample", "storage", "weight")


class DescriptionsUserListSerializer(serializers.ModelSerializer):
    class Meta:
        model = DescriptionsUserList
        fields = ("id", "name")


# class DescriptionsUserListElementSerializer(serializers.ModelSerializer):
#     expressions = DescriptionSerializer(source="description")


#     class Meta:
#         model = DescriptionsUserListElement
#         fields = ("description", "expressions")
class DescriptionsUserListElementSerializer(serializers.ModelSerializer):
    description = DescriptionSerializer(read_only=True)

    class Meta:
        model = DescriptionsUserListElement
        fields = ("pk", "description")
