from rest_framework import serializers

from parameters.models import SpeciesParameter
from register.models import PlantSpecies, PlantVariety

class SpeciesParamSerializer(serializers.ModelSerializer):
    name = serializers.StringRelatedField(many=False, source="parameter")

    class Meta:
        model = SpeciesParameter
        fields = ["name", "value"]

class PlantSpeciesSerializer(serializers.ModelSerializer):
    speciesparameter = SpeciesParamSerializer(
        many=True, read_only=True, source="speciesparameter_set"
    )

    class Meta:
        model = PlantSpecies
        fields = ["common_name", "latin_name", "speciesparameter"]

class PlantVarietySerializer(serializers.ModelSerializer):
    class Meta:
        model = PlantVariety
        fields = '__all__'
