from rest_framework import serializers

from collect.models import Germinability, SampleWeight, SeedSample, StoragePosition

class StoragePositionSerializer(serializers.ModelSerializer):
    class Meta:
        model = StoragePosition
        fields = '__all__'

class GerminabilitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Germinability
        fields = ['germinability', 'after_days', 'performed_at']

class SampleWeightSerializer(serializers.ModelSerializer):
    class Meta:
        model = SampleWeight
        fields = ['weight', 'created_at']

class SeedSampleSerializer(serializers.ModelSerializer):
    variety = serializers.StringRelatedField()
    position = serializers.StringRelatedField()
    # weight = SampleWeightSerializer(many=True, read_only=True, source="sampleweight_set")
    # germinability = GerminabilitySerializer(many=True, read_only=True, source="germinability_set")
    class Meta:
        model = SeedSample
        fields = ['sample_id', 'variety', 'position', 'weight', 'germinability']
