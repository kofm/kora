from rest_framework import serializers

from register.models import PlantVariety, PlantVarietyName

class PlantVarietyNameSerializer(serializers.ModelSerializer):
    class Meta:
        model = PlantVarietyName
        fields = ['name', ]

class PlantVarietySerializer(serializers.ModelSerializer):
    names = PlantVarietyNameSerializer(many = True, read_only=True, source="names")
    class Meta:
        model = PlantVariety
        fields = ['id', 'names']
