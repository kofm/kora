from register.models import PlantSpecies
from parameters.models import CropParameter, Parameter
from rest_framework import serializers

class CropParamSerializer(serializers.ModelSerializer):
    name = serializers.StringRelatedField(many=False, source = 'parameter')
    class Meta:
        model = CropParameter
        fields = ['name', 'value']

class CropSerializer(serializers.ModelSerializer):
    cropparameter = CropParamSerializer(many=True, read_only=True, source = 'cropparameter_set')
    class Meta:
        model = PlantSpecies
        fields = ['common_name', 'latin_name', 'cropparameter']

