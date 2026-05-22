from django.db import transaction
from django_countries.serializers import CountryFieldMixin
from rest_framework import serializers

from collect.models import Cart, CartItem, Sample, Storage, StoragePosition
from describe.models import (
    Description,
    Expression,
    Protocol,
    State,
    StateGroup,
    Trait,
    Workspace,
    WorkspaceElement,
)
from parameters.models import Parameter, VarietalParameter
from register.models import Entity, PlantSpecies, PlantVariety, PlantVarietyName, Protection, ProtectionType
from restapi.serializers.generic import BulkModelSerializer


class PlantSpeciesSerializer(BulkModelSerializer):
    class Meta:
        model = PlantSpecies
        fields = ("id", "common_name", "latin_name", "plant_type")


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
    species_common_name = serializers.CharField(source="species.common_name", read_only=True)
    names = PlantVarietyNameSerializer(many=True, read_only=True)

    class Meta(BulkModelSerializer.Meta):
        list_serializer_class = PlantVarietyListSerializer
        model = PlantVariety
        fields = (
            "id",
            "name",
            "species",
            "species_common_name",
            "names",
            "created_at",
            "updated_at",
        )


class EntitySerializer(BulkModelSerializer, CountryFieldMixin, serializers.ModelSerializer):
    class Meta(BulkModelSerializer.Meta):
        model = Entity
        fields = (
            "id",
            "name",
            "type",
            "country",
            "contact",
            "email",
        )


class ProtectionSerializer(CountryFieldMixin, BulkModelSerializer):
    type = serializers.SlugRelatedField(
        slug_field="code",
        queryset=ProtectionType.objects.all(),
    )

    class Meta(BulkModelSerializer.Meta):
        model = Protection
        fields = (
            "id",
            "type",
            "reference",
            "status",
            "country",
            "variety",
            "applicants",
            "maintainers",
            "date_start",
            "date_end",
            "note",
        )


class ProtocolSerializer(BulkModelSerializer):
    class Meta(BulkModelSerializer.Meta):
        model = Protocol
        fields = ("id", "name", "plantspecies", "url_ref")


class StateListSerializer(serializers.ListSerializer):
    @transaction.atomic
    def create(self, validated_data):
        groups = StateGroup.objects.bulk_create(StateGroup() for _ in validated_data)
        states = [State(group=group, **item) for item, group in zip(validated_data, groups, strict=True)]
        return State.objects.bulk_create(states)


class StateSerializer(BulkModelSerializer):
    group = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta(BulkModelSerializer.Meta):
        model = State
        fields = ("id", "numeric_id", "description", "trait", "group")
        list_serializer_class = StateListSerializer

    @transaction.atomic
    def create(self, validated_data):
        validated_data["group"] = StateGroup.objects.create()
        return super().create(validated_data)


class TraitSerializer(BulkModelSerializer):
    class Meta(BulkModelSerializer.Meta):
        model = Trait
        fields = (
            "id",
            "numeric_id",
            "description",
            "protocol",
        )


class DescriptionSerializer(BulkModelSerializer):
    variety_name = serializers.CharField(source="variety.name", read_only=True)
    species = serializers.StringRelatedField(source="variety.species.latin_name", read_only=True)
    protocol_name = serializers.StringRelatedField(source="protocol.name", read_only=True)

    class Meta:
        model = Description
        fields = (
            "id",
            "name",
            "variety",
            "variety_name",
            "species",
            "protocol",
            "protocol_name",
        )


class ExpressionSerializer(BulkModelSerializer):
    description = serializers.PrimaryKeyRelatedField(queryset=Description.objects.select_related("variety__species"))
    trait_id = serializers.IntegerField(source="state.trait.id", read_only=True)
    trait_description = serializers.StringRelatedField(many=False, source="state.trait", read_only=True)
    trait_numeric_id = serializers.IntegerField(source="state.trait.numeric_id", read_only=True)
    state_description = serializers.StringRelatedField(many=False, source="state", read_only=True)
    state_group = serializers.IntegerField(source="state.group_id", read_only=True)

    class Meta(BulkModelSerializer.Meta):
        model = Expression
        fields = (
            "description",
            "trait_id",
            "trait_numeric_id",
            "trait_description",
            "state",
            "state_description",
            "state_group",
            "note",
        )


class ParameterSerializer(BulkModelSerializer):
    class Meta(BulkModelSerializer.Meta):
        model = Parameter
        fields = ("id", "code", "name", "description", "measure_unit")


class VarietalParameterSerializer(BulkModelSerializer):
    parameter_code = serializers.StringRelatedField(many=False, source="parameter", read_only=True)

    class Meta(BulkModelSerializer.Meta):
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
    class Meta(BulkModelSerializer.Meta):
        model = Storage
        fields = ("id", "name", "order")


class StoragePositionSerializer(BulkModelSerializer):
    storage = serializers.StringRelatedField(many=False, read_only=True)

    class Meta(BulkModelSerializer.Meta):
        model = StoragePosition
        fields = ("id", "name", "storage")

    def get_storage_verbose_name(self, obj):
        return str(obj)


class SampleSerializer(BulkModelSerializer):
    storage_name = serializers.StringRelatedField(many=False, read_only=True, source="position.storage")
    position_name = serializers.StringRelatedField(many=False, source="position.name")
    last_weight = serializers.FloatField(read_only=True)
    available_weight = serializers.FloatField(read_only=True)
    last_germinability = serializers.FloatField(read_only=True)

    class Meta(BulkModelSerializer.Meta):
        model = Sample
        fields = (
            "id",
            "sample_id",
            "variety",
            "position",
            "storage_name",
            "position_name",
            "growing_season",
            "last_weight",
            "available_weight",
            "last_germinability",
            "notes",
        )


class CartItemSerializer(BulkModelSerializer):
    sample_id = serializers.IntegerField(source="sample.sample_id", read_only=True)
    variety_name = serializers.CharField(source="sample.variety.name", read_only=True)
    species = serializers.CharField(source="sample.variety.species.common_name", read_only=True)
    variety = serializers.IntegerField(source="sample.variety.pk", read_only=True)
    storage = serializers.CharField(source="sample.position.storage", read_only=True)
    position = serializers.CharField(source="sample.position.name", read_only=True)

    class Meta(BulkModelSerializer.Meta):
        model = CartItem
        fields = (
            "sample",
            "sample_id",
            "variety",
            "variety_name",
            "species",
            "storage",
            "position",
            "weight",
            "order",
        )


class WorkspaceSerializer(BulkModelSerializer):
    class Meta(BulkModelSerializer.Meta):
        model = Workspace
        fields = ("id", "name")


class CartSerializer(BulkModelSerializer):
    class Meta(BulkModelSerializer.Meta):
        model = Cart
        fields = ("id", "name")


class ExpressionNestedSerializer(serializers.ModelSerializer):
    trait_id = serializers.IntegerField(source="state.trait.numeric_id")
    trait_description = serializers.StringRelatedField(many=False, source="state.trait.description")
    state_id = serializers.IntegerField(source="state.numeric_id")
    state_description = serializers.StringRelatedField(many=False, source="state.description")

    class Meta(BulkModelSerializer.Meta):
        model = Expression
        fields = ("trait_id", "trait_description", "state_id", "state_description", "note")


class DescriptionNestedSerializer(serializers.ModelSerializer):
    expressions = ExpressionNestedSerializer(many=True, read_only=True)

    class Meta(BulkModelSerializer.Meta):
        model = Description
        fields = ("name", "expressions")


class WorkspaceElementSerializer(BulkModelSerializer):
    description = DescriptionNestedSerializer(read_only=True)

    class Meta(BulkModelSerializer.Meta):
        model = WorkspaceElement
        fields = ("id", "description")
