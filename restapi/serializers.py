from django_countries.serializers import CountryFieldMixin
from rest_framework import serializers

from collect.models import Cart, CartItem, Sample, Storage, StoragePosition
from describe.models import (
    Description,
    Expression,
    Protocol,
    State,
    Trait,
    Workspace,
    WorkspaceElement,
)
from parameters.models import Parameter, VarietalParameter
from register.models import Entity, PlantSpecies, PlantVariety, PlantVarietyName, Protection


class BulkListSerializer(serializers.ListSerializer):
    def create(self, validated_data):
        model_class = self.child.Meta.model
        return model_class.objects.bulk_create([model_class(**item) for item in validated_data])


class BulkModelSerializer(serializers.ModelSerializer):
    class Meta:
        list_serializer_class = BulkListSerializer


class PlantSpeciesSerializer(BulkModelSerializer):
    class Meta:
        model = PlantSpecies
        fields = ("pk", "common_name", "latin_name", "plant_type")


class PlantVarietyNameSerializer(BulkModelSerializer):
    class Meta:
        model = PlantVarietyName
        fields = ("name", "change_date")


class PlantVarietyListSerializer(serializers.ListSerializer):
    def create(self, validated_data):
        varieties = PlantVariety.objects.bulk_create([PlantVariety(**item) for item in validated_data])
        PlantVarietyName.objects.bulk_create(
            [PlantVarietyName(variety=variety, name=variety.name) for variety in varieties]
        )
        return varieties


class PlantVarietySerializer(serializers.ModelSerializer):
    names = PlantVarietyNameSerializer(many=True, read_only=True)

    class Meta(BulkModelSerializer.Meta):
        list_serializer_class = PlantVarietyListSerializer
        model = PlantVariety
        fields = ("pk", "name", "species", "names")


class EntitySerializer(BulkModelSerializer, CountryFieldMixin, serializers.ModelSerializer):
    class Meta(BulkModelSerializer.Meta):
        model = Entity
        fields = (
            "pk",
            "name",
            "type",
            "country",
            "contact",
            "email",
        )


class ProtectionSerializer(CountryFieldMixin, BulkModelSerializer):
    class Meta(BulkModelSerializer.Meta):
        model = Protection
        fields = (
            "pk",
            "type",
            "reference",
            "status",
            "country",
            "variety",
            "applicants",
            "maintainers",
            "date_start",
            "date_end",
        )


class ProtocolSerializer(BulkModelSerializer):
    class Meta:
        model = Protocol
        fields = ("pk", "name", "plantspecies", "url_ref")


class StateSerializer(BulkModelSerializer):
    class Meta:
        model = State
        fields = ("pk", "numeric_id", "description", "trait")


class TraitSerializer(BulkModelSerializer):
    states = StateSerializer(many=True, read_only=True)

    class Meta:
        model = Trait
        fields = ("pk", "numeric_id", "description", "protocol", "states")


class DescriptionExpressionSerializer(serializers.ModelSerializer):
    trait = serializers.StringRelatedField(many=False, source="state.trait", read_only=True)
    trait_id = serializers.IntegerField(source="state.trait.numeric_id")
    state_id = serializers.IntegerField(source="state.numeric_id")
    state_description = serializers.StringRelatedField(many=False, source="state", read_only=True)

    class Meta:
        model = Expression
        fields = ("state", "state_id", "trait", "trait_id", "state_description", "note")


class DescriptionSerializer(BulkModelSerializer):
    variety_name = serializers.CharField(source="variety.name", read_only=True)
    species = serializers.StringRelatedField(source="variety.species.latin_name", read_only=True)
    protocol_name = serializers.StringRelatedField(source="protocol.name", read_only=True)
    expressions = DescriptionExpressionSerializer(many=True, read_only=True)

    class Meta:
        model = Description
        fields = (
            "pk",
            "name",
            "variety",
            "variety_name",
            "species",
            "protocol",
            "protocol_name",
            "expressions",
        )


class ExpressionSerializer(BulkModelSerializer):
    class Meta:
        model = Expression
        fields = ("description", "state", "note")


class ParameterSerializer(BulkModelSerializer):
    class Meta:
        model = Parameter
        fields = ("pk", "code", "name", "description", "measure_unit")


class VarietalParameterSerializer(BulkModelSerializer):
    parameter_code = serializers.StringRelatedField(many=False, source="parameter", read_only=True)

    class Meta:
        model = VarietalParameter
        fields = (
            "value",
            "variety",
            "parameter",
            "parameter_code",
            "created_at",
            "updated_at",
            "note",
            "url_ref",
        )


class StorageSerializer(BulkModelSerializer):
    class Meta:
        model = Storage
        fields = ("pk", "name", "order")


class StoragePositionSerializer(BulkModelSerializer):
    storage = serializers.StringRelatedField(many=False, read_only=True)

    class Meta:
        model = StoragePosition
        fields = ("pk", "name", "storage")

    def get_storage_verbose_name(self, obj):
        return str(obj)


class SampleSerializer(BulkModelSerializer):
    storage = serializers.StringRelatedField(many=False, read_only=True, source="position.storage")
    position_name = serializers.StringRelatedField(many=False, source="position.name")
    last_weight = serializers.FloatField(read_only=True)
    available_weight = serializers.FloatField(read_only=True)
    last_germinability = serializers.FloatField(read_only=True)

    class Meta:
        model = Sample
        fields = (
            "pk",
            "sample_id",
            "variety",
            "notes",
            "growing_season",
            "storage",
            "position",
            "position_name",
            "last_weight",
            "available_weight",
            "last_germinability",
        )


class CartItemSerializer(BulkModelSerializer):
    sample_id = serializers.IntegerField(source="sample.sample_id", read_only=True)
    variety_name = serializers.CharField(source="sample.variety.name", read_only=True)
    species = serializers.CharField(source="sample.variety.species.common_name", read_only=True)
    variety_id = serializers.IntegerField(source="sample.variety.pk", read_only=True)
    storage = serializers.CharField(source="sample.position.storage", read_only=True)
    position = serializers.CharField(source="sample.position.name", read_only=True)

    class Meta:
        model = CartItem
        fields = (
            "variety_id",
            "variety_name",
            "species",
            "sample",
            "sample_id",
            "storage",
            "position",
            "weight",
            "order",
        )


class WorkspaceSerializer(BulkModelSerializer):
    class Meta:
        model = Workspace
        fields = ("id", "name")


class CartSerializer(BulkModelSerializer):
    class Meta:
        model = Cart
        fields = ("id", "name")


class WorkspaceElementSerializer(BulkModelSerializer):
    description = DescriptionSerializer(read_only=True)

    class Meta:
        model = WorkspaceElement
        fields = ("pk", "description")
