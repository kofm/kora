from rest_framework import serializers
from django_countries.serializers import CountryFieldMixin

from parameters.models import SpeciesParameter
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
        fields = ["id", "species", "name", "names"]


class EntitySerializer(CountryFieldMixin, serializers.ModelSerializer):
    class Meta:
        model = Entity
        fields = "__all__"


class ProtectionSerializer(CountryFieldMixin, serializers.ModelSerializer):
    species = serializers.CharField(read_only=True)

    class Meta:
        model = Protection
        fields = "__all__"
