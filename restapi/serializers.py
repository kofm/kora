import math

from rest_framework import serializers
from django_countries.serializers import CountryFieldMixin
from collect.models import CartItem, SeedSample, StoragePosition
from describe.models import Description, Expression, Protocol, Trait, State

from parameters.models import SpeciesParameter, VarietalParameter
from register.models import Entity, PlantSpecies, PlantVariety, PlantVarietyName, Protection


class SpeciesParamSerializer(serializers.ModelSerializer):
    name = serializers.StringRelatedField(many=False, source="parameter")

    class Meta:
        model = SpeciesParameter
        fields = ["name", "value"]


class PlantSpeciesSerializer(serializers.ModelSerializer):
    speciesparameter = SpeciesParamSerializer(many=True, read_only=True, source="parameters")

    class Meta:
        model = PlantSpecies
        fields = ["common_name", "latin_name", "speciesparameter"]


class PlantVarietyNameSerializer(serializers.ModelSerializer):
    class Meta:
        model = PlantVarietyName
        fields = [
            "name",
        ]


class PlantVarietySerializer(serializers.ModelSerializer):
    names = PlantVarietyNameSerializer(many=True, read_only=True)

    class Meta:
        model = PlantVariety
        fields = [
            "id",
            "name",
            "species",
            "breeder",
            "names",
        ]


class EntitySerializer(CountryFieldMixin, serializers.ModelSerializer):
    class Meta:
        model = Entity
        fields = "__all__"


class ProtectionSerializer(CountryFieldMixin, serializers.ModelSerializer):
    species = serializers.CharField(read_only=True)

    class Meta:
        model = Protection
        fields = "__all__"


class VarietalParameterSerializer(serializers.ModelSerializer):
    variety_name = serializers.StringRelatedField(many=False, source="variety", read_only=True)
    parameter_code = serializers.StringRelatedField(many=False, source="parameter", read_only=True)

    class Meta:
        model = VarietalParameter
        fields = "__all__"


class SeedSampleSerializer(serializers.ModelSerializer):
    last_germinability = serializers.SerializerMethodField()
    last_weight = serializers.SerializerMethodField()

    class Meta:
        model = SeedSample
        fields = "__all__"  # This would already include all the fields from the model.

    def get_last_germinability(self, obj):
        germinability = obj.germinability
        return 0.0 if germinability is None or math.isnan(germinability) else germinability

    def get_last_weight(self, obj):
        weight = obj.weight
        return 0.0 if weight is None or math.isnan(weight) else weight


class CartSerializer(serializers.ModelSerializer):
    variety_name = serializers.CharField(source="sample.variety.name", read_only=True)
    variety_id = serializers.IntegerField(source="sample.variety.pk", read_only=True)
    storage = serializers.CharField(source="sample.position")

    class Meta:
        model = CartItem
        fields = ("variety_name", "variety_id", "sample", "storage", "weight")


class StoragePositionSerializer(serializers.ModelSerializer):
    storage_verbose_name = serializers.SerializerMethodField()

    class Meta:
        model = StoragePosition
        fields = "__all__"

    def get_storage_verbose_name(self, obj):
        return str(obj)


class ProtocolSerializer(serializers.ModelSerializer):
    class Meta:
        model = Protocol
        fields = ("pk", "name")


class StateSerializer(serializers.ModelSerializer):
    class Meta:
        model = State
        fields = ("pk", "numeric_id", "description")


class TraitSerializer(serializers.ModelSerializer):
    class Meta:
        model = Trait
        fields = ("pk", "numeric_id", "description")


class ExpressionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Expression
        fields = ("description", "state", "note")


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
