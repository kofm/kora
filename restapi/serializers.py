from rest_framework import serializers
from django_countries.serializers import CountryFieldMixin
from collect.models import SeedSample
import math

from parameters.models import SpeciesParameter, VarietalParameter
from register.models import Entity, PlantSpecies, PlantVariety, PlantVarietyName, Protection


class SpeciesParamSerializer(serializers.ModelSerializer):
    name = serializers.StringRelatedField(many=False, source="parameter")

    class Meta:
        model = SpeciesParameter
        fields = ["name", "value"]


class PlantSpeciesSerializer(serializers.ModelSerializer):
    speciesparameter = SpeciesParamSerializer(
        many=True, read_only=True, source="parameters"
    )

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
    species = serializers.StringRelatedField(many=False)
    names = PlantVarietyNameSerializer(many=True, read_only=True)

    class Meta:
        model = PlantVariety
        fields = ["id", "name", "species", "breeder", "names",]


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
