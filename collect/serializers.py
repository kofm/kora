from rest_framework import serializers

from collect.models import StoragePosition

class StoragePositionSerializer(serializers.ModelSerializer):
    class Meta:
        model = StoragePosition
        fields = '__all__'
