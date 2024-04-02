from rest_framework import serializers

from collect.models import Germinability, SampleWeight, SeedSample, StoragePosition


class StoragePositionSerializer(serializers.ModelSerializer):
    class Meta:
        model = StoragePosition
        fields = "__all__"


class GerminabilitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Germinability
        fields = ["germinability", "after_days", "performed_at"]


class SampleWeightSerializer(serializers.ModelSerializer):
    class Meta:
        model = SampleWeight
        fields = ["weight", "seedsample"]


class SeedSampleSerializer(serializers.ModelSerializer):
    variety = serializers.StringRelatedField()
    position = serializers.StringRelatedField()

    class Meta:
        model = SeedSample
        fields = ["sample_id", "variety", "position"]
