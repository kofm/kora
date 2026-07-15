from rest_framework import serializers

from collect.models import Germinability, Sample, SampleWeight


class GerminabilitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Germinability
        fields = ["sample", "germinability", "after_days", "performed_at"]


class SampleWeightSerializer(serializers.ModelSerializer):
    class Meta:
        model = SampleWeight
        fields = ["sample", "weight", "created_at"]


class SampleSerializer(serializers.ModelSerializer):
    variety = serializers.StringRelatedField()
    position = serializers.StringRelatedField()

    class Meta:
        model = Sample
        fields = ["sample_id", "variety", "position"]
