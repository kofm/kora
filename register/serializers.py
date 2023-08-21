from rest_framework import serializers

from register.models import Entity, PlantVariety, PlantVarietyName, Protection

class PlantVarietyNameSerializer(serializers.ModelSerializer):
    class Meta:
        model = PlantVarietyName
        fields = ['name', ]

class PlantVarietySerializer(serializers.ModelSerializer):
    names = PlantVarietyNameSerializer(many = True, read_only=True, source="names")
    class Meta:
        model = PlantVariety
        fields = ['id', 'names']


class ProtectionSerializer(serializers.ModelSerializer):
    species = serializers.CharField(read_only=True)
    class Meta:
        model = Protection
        fields = '__all__'


class EntitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Entity
        fields = '__all__'
