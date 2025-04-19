from rest_framework import serializers

from calculator.models import Crop, CropParameter
from parameters.models import Parameter
from register.models import PlantSpecies, PlantVariety
from spaces.models import Area


class CropSpecieSerializer(serializers.ModelSerializer):
    class Meta:
        model = PlantSpecies
        fields = ["common_name", "latin_name"]


class CropVarietySerializer(serializers.ModelSerializer):
    class Meta:
        model = PlantVariety
        fields = ["name"]


class CropObjectRelatedField(serializers.RelatedField):
    def to_representation(self, value):
        if isinstance(value, PlantSpecies):
            serializer = CropSpecieSerializer(value)
        elif isinstance(value, PlantVariety):
            serializer = CropVarietySerializer(value)
        else:
            raise Exception("Unexpected type of crop")
        return serializer.data


class CropSerializer(serializers.ModelSerializer):
    content_object = CropObjectRelatedField(read_only=True)

    class Meta:
        model = Crop
        fields = [
            "id",
            "content_type",
            "content_object",
            "notes",
        ]


class AreaSerializer(serializers.ModelSerializer):
    crops = CropSerializer(many=True, source="crop_set")

    class Meta:
        model = Area
        fields = "__all__"


class ParameterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Parameter
        fields = "__all__"


class CropParameterSerializer(serializers.ModelSerializer):
    parameter_data = ParameterSerializer(many=False, read_only=True, source="parameter")

    class Meta:
        model = CropParameter
        fields = ["id", "crop", "value", "parameter", "parameter_data"]
