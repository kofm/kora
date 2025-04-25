from rest_framework import serializers

from collect.models import Germinability, Sample, SampleWeight, StoragePosition


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
        fields = ["weight", "sample"]


class SampleSerializer(serializers.ModelSerializer):
    variety = serializers.StringRelatedField()
    position = serializers.StringRelatedField()

    class Meta:
        model = Sample
        fields = ["sample_id", "variety", "position"]
