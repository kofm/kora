from rest_framework import serializers

from calculator.models import Crop, CropLayout, CropParameter
from parameters.models import Parameter
from register.models import PlantVariety
from restapi.fields import MappedPrimaryKeyRelatedField
from restapi.serializers.generic import BaseSpreadsheetImportRequestSerializer


class CropVarietySerializer(serializers.ModelSerializer):
    class Meta:
        model = PlantVariety
        fields = ["name"]


class CropSerializer(serializers.ModelSerializer):
    variety_data = CropVarietySerializer(source="variety", read_only=True)

    class Meta:
        model = Crop
        fields = ["id", "layout", "variety", "variety_data", "order", "notes", "created_at", "updated_at"]


class CropLayoutSerializer(serializers.ModelSerializer):
    crops = CropSerializer(many=True, read_only=True)

    class Meta:
        model = CropLayout
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


class CropImportListSerializer(serializers.ListSerializer):
    def to_internal_value(self, data):
        self.context["variety_map"] = PlantVariety.objects.in_bulk()
        self.context["layout_map"] = CropLayout.objects.visible().in_bulk()
        return super().to_internal_value(data)


class CropImportRowSerializer(serializers.Serializer):
    notes = serializers.CharField(required=False)
    variety = MappedPrimaryKeyRelatedField(mapping_key="variety_map", required=True)
    layout = MappedPrimaryKeyRelatedField(mapping_key="layout_map", required=True)
    order = serializers.IntegerField(min_value=0, required=False, default=0)

    class Meta:
        list_serializer_class = CropImportListSerializer

    def create(self, validated_data):
        return Crop(**validated_data)


class CropImportRequestSerializer(BaseSpreadsheetImportRequestSerializer):
    row_serializer = CropImportRowSerializer
