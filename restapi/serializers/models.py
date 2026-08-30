from django.core.exceptions import ValidationError as DjangoValidationError
from django.db import transaction
from django_countries.serializers import CountryFieldMixin
from rest_framework import serializers

from calculator.models import (
    Crop,
    CropLayout,
    FieldBook,
    ParameterObservation,
    ParameterTarget,
    TraitObservation,
    TraitTarget,
)
from calculator.targets import TargetPlan, TargetPlanValidationError, create_targets, validate_target_identity
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
    class Meta(BulkModelSerializer.Meta):
        model = PlantSpecies
        fields = ("id", "common_name", "latin_name", "plant_type")


class PlantVarietyNameSerializer(BulkModelSerializer):
    class Meta(BulkModelSerializer.Meta):
        model = PlantVarietyName
        fields = ("name", "change_date")


class PlantVarietyListSerializer(serializers.ListSerializer):
    @transaction.atomic
    def create(self, validated_data):
        varieties = PlantVariety.objects.bulk_create([PlantVariety(**item) for item in validated_data])
        PlantVarietyName.objects.bulk_create(
            [PlantVarietyName(variety=variety, name=variety.name) for variety in varieties]
        )
        return varieties


class PlantVarietySerializer(BulkModelSerializer):
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

    @transaction.atomic
    def create(self, validated_data):
        variety = super().create(validated_data)
        PlantVarietyName.objects.create(
            variety=variety,
            name=variety.name,
        )
        return variety


class EntitySerializer(CountryFieldMixin, BulkModelSerializer):
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


class ProtectionTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProtectionType
        fields = ("id", "code", "name")


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
            "grouping",
            "protocol",
        )


class DescriptionSerializer(BulkModelSerializer):
    variety_name = serializers.CharField(source="variety.name", read_only=True)
    species = serializers.CharField(source="variety.species.latin_name", read_only=True)
    protocol_name = serializers.CharField(source="protocol.name", read_only=True)
    label_name = serializers.CharField(source="label.name", read_only=True)

    class Meta(BulkModelSerializer.Meta):
        model = Description
        fields = (
            "id",
            "label",
            "label_name",
            "variety",
            "variety_name",
            "species",
            "protocol",
            "protocol_name",
        )


class ExpressionSerializer(BulkModelSerializer):
    trait = serializers.IntegerField(source="state.trait_id", read_only=True)
    trait_numeric_id = serializers.IntegerField(source="state.trait.numeric_id", read_only=True)
    trait_description = serializers.CharField(source="state.trait.description", read_only=True)
    state_numeric_id = serializers.IntegerField(source="state.numeric_id", read_only=True)
    state_description = serializers.CharField(source="state.description", read_only=True)
    state_group = serializers.IntegerField(source="state.group_id", read_only=True)

    class Meta(BulkModelSerializer.Meta):
        model = Expression
        fields = (
            "id",
            "description",
            "trait",
            "trait_numeric_id",
            "trait_description",
            "state",
            "state_numeric_id",
            "state_description",
            "state_group",
            "note",
        )


class ParameterSerializer(BulkModelSerializer):
    class Meta(BulkModelSerializer.Meta):
        model = Parameter
        fields = ("id", "code", "name", "description", "measure_unit")


class VarietalParameterSerializer(BulkModelSerializer):
    parameter_code = serializers.CharField(source="parameter.code", read_only=True)

    class Meta(BulkModelSerializer.Meta):
        model = VarietalParameter
        fields = (
            "id",
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
    storage_name = serializers.CharField(source="storage.name", read_only=True)

    class Meta(BulkModelSerializer.Meta):
        model = StoragePosition
        fields = ("id", "name", "storage", "storage_name")


class SampleSerializer(BulkModelSerializer):
    sample_number = serializers.IntegerField(source="sample_id")
    species_common_name = serializers.CharField(source="variety.species.common_name", read_only=True)
    variety_name = serializers.CharField(source="variety.name", read_only=True)
    position_display = serializers.StringRelatedField(source="position", read_only=True)
    last_weight = serializers.FloatField(read_only=True)
    available_weight = serializers.FloatField(read_only=True)
    last_germinability = serializers.FloatField(read_only=True)

    class Meta(BulkModelSerializer.Meta):
        model = Sample
        fields = (
            "id",
            "sample_number",
            "species_common_name",
            "variety",
            "variety_name",
            "position",
            "position_display",
            "growing_season",
            "last_weight",
            "available_weight",
            "last_germinability",
            "notes",
        )


class CartItemSerializer(BulkModelSerializer):
    sample_number = serializers.IntegerField(source="sample.sample_id", read_only=True)
    species_common_name = serializers.CharField(source="sample.variety.species.common_name", read_only=True)
    variety = serializers.IntegerField(source="sample.variety_id", read_only=True)
    variety_name = serializers.CharField(source="sample.variety.name", read_only=True)
    position = serializers.IntegerField(source="sample.position_id", read_only=True, allow_null=True)
    position_display = serializers.StringRelatedField(source="sample.position", read_only=True)

    class Meta(BulkModelSerializer.Meta):
        model = CartItem
        fields = (
            "id",
            "sample",
            "sample_number",
            "species_common_name",
            "variety",
            "variety_name",
            "position",
            "position_display",
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
    trait = serializers.IntegerField(source="state.trait_id", read_only=True)
    trait_numeric_id = serializers.IntegerField(source="state.trait.numeric_id", read_only=True)
    trait_description = serializers.CharField(source="state.trait.description", read_only=True)
    state_numeric_id = serializers.IntegerField(source="state.numeric_id", read_only=True)
    state_description = serializers.CharField(source="state.description", read_only=True)

    class Meta:
        model = Expression
        fields = (
            "trait",
            "trait_numeric_id",
            "trait_description",
            "state",
            "state_numeric_id",
            "state_description",
            "note",
        )


class DescriptionNestedSerializer(serializers.ModelSerializer):
    variety_name = serializers.CharField(source="variety.name", read_only=True)
    label_name = serializers.CharField(source="label.name", read_only=True)
    protocol_name = serializers.CharField(source="protocol.name", read_only=True)
    expressions = ExpressionNestedSerializer(many=True, read_only=True)

    class Meta:
        model = Description
        fields = ("label", "label_name", "variety", "variety_name", "protocol", "protocol_name", "expressions")


class ObservationSerializer(serializers.ModelSerializer):
    crop = serializers.PrimaryKeyRelatedField(queryset=Crop.objects.mutable())
    crop_display = serializers.StringRelatedField(source="crop", read_only=True)
    layout = serializers.IntegerField(source="crop.layout_id", read_only=True)
    layout_name = serializers.CharField(source="crop.layout.name", read_only=True)
    location = serializers.IntegerField(source="crop.layout.location_id", read_only=True)
    location_name = serializers.CharField(source="crop.layout.location.name", read_only=True)
    variety = serializers.IntegerField(source="crop.variety_id", read_only=True)
    variety_name = serializers.CharField(source="crop.variety.name", read_only=True)
    species = serializers.IntegerField(source="crop.variety.species_id", read_only=True)
    species_common_name = serializers.CharField(source="crop.variety.species.common_name", read_only=True)
    step = serializers.PrimaryKeyRelatedField(read_only=True, allow_null=True)
    step_display = serializers.StringRelatedField(source="step", read_only=True)
    created_by = serializers.PrimaryKeyRelatedField(read_only=True)
    created_by_display = serializers.StringRelatedField(source="created_by", read_only=True)

    class Meta:
        abstract = True


class FieldBookSerializer(serializers.ModelSerializer):
    layout_name = serializers.CharField(source="layout.name", read_only=True)
    location = serializers.PrimaryKeyRelatedField(source="layout.location", read_only=True)
    location_name = serializers.CharField(source="layout.location.name", read_only=True)

    class Meta:
        model = FieldBook
        fields = ("id", "name", "layout", "layout_name", "location", "location_name")

    def get_fields(self):
        fields = super().get_fields()

        if self.instance is not None:
            fields["layout"].read_only = True

        return fields

    def validate_layout(self, layout):
        if layout.is_archived:
            raise serializers.ValidationError("Fieldbooks cannot be added to an archived layout.")
        return layout


class TraitObservationSerializer(ObservationSerializer):
    state_display = serializers.StringRelatedField(source="state", read_only=True)
    trait = serializers.IntegerField(source="state.trait_id", read_only=True)
    trait_numeric_id = serializers.IntegerField(source="state.trait.numeric_id", read_only=True)
    trait_description = serializers.CharField(source="state.trait.description", read_only=True)
    protocol = serializers.IntegerField(source="state.trait.protocol_id", read_only=True)
    protocol_name = serializers.CharField(source="state.trait.protocol.name", read_only=True)

    class Meta:
        model = TraitObservation
        fields = (
            "id",
            "crop",
            "crop_display",
            "layout",
            "layout_name",
            "location",
            "location_name",
            "variety",
            "variety_name",
            "species",
            "species_common_name",
            "step",
            "step_display",
            "state",
            "state_display",
            "trait",
            "trait_numeric_id",
            "trait_description",
            "protocol",
            "protocol_name",
            "recorded_at",
            "created_by",
            "created_by_display",
            "notes",
        )

    def validate(self, attrs):
        crop = attrs.get("crop")
        state = attrs.get("state")
        if crop and state and crop.variety.species_id != state.trait.protocol.plantspecies_id:
            raise serializers.ValidationError({"state": "The state trait species must match the crop variety species."})
        return attrs


class ParameterObservationSerializer(ObservationSerializer):
    parameter_code = serializers.CharField(source="parameter.code", read_only=True)
    parameter_name = serializers.CharField(source="parameter.name", read_only=True)
    parameter_display = serializers.StringRelatedField(source="parameter", read_only=True)

    class Meta:
        model = ParameterObservation
        fields = (
            "id",
            "crop",
            "crop_display",
            "layout",
            "layout_name",
            "location",
            "location_name",
            "variety",
            "variety_name",
            "species",
            "species_common_name",
            "step",
            "step_display",
            "parameter",
            "parameter_code",
            "parameter_name",
            "parameter_display",
            "parameter_value",
            "parameter_date",
            "recorded_at",
            "created_by",
            "created_by_display",
            "notes",
        )

    def validate(self, attrs):
        if attrs.get("parameter_value") is None and attrs.get("parameter_date") is None:
            raise serializers.ValidationError("At least one of parameter_value or parameter_date is required.")
        return attrs


class WorkspaceElementSerializer(BulkModelSerializer):
    description_detail = DescriptionNestedSerializer(source="description", read_only=True)

    class Meta(BulkModelSerializer.Meta):
        model = WorkspaceElement
        fields = ("id", "description", "description_detail", "order")


class CropLayoutSerializer(BulkModelSerializer):
    location_name = serializers.CharField(source="location.name", read_only=True)

    class Meta(BulkModelSerializer.Meta):
        model = CropLayout
        fields = (
            "id",
            "location",
            "location_name",
            "name",
            "description",
            "ncol",
            "archived_at",
            "created_at",
            "updated_at",
        )
        read_only_fields = ("archived_at",)


class CropSerializer(BulkModelSerializer):
    variety_name = serializers.CharField(source="variety.name", read_only=True)
    species = serializers.IntegerField(source="variety.species_id", read_only=True)
    species_common_name = serializers.CharField(source="variety.species.common_name", read_only=True)
    layout_name = serializers.CharField(source="layout.name", read_only=True)

    class Meta(BulkModelSerializer.Meta):
        model = Crop
        fields = (
            "id",
            "variety",
            "variety_name",
            "species",
            "species_common_name",
            "layout",
            "layout_name",
            "order",
            "created_at",
            "updated_at",
            "notes",
        )

    def validate_layout(self, layout):
        if self.instance and layout.pk != self.instance.layout_id:
            raise serializers.ValidationError("The crop layout cannot be changed.")
        if layout.is_archived:
            raise serializers.ValidationError("Crops cannot be added to an archived layout.")
        return layout

    def validate_variety(self, variety):
        if self.instance and variety.species_id != self.instance.variety.species_id:
            raise serializers.ValidationError("The crop variety species cannot be changed.")
        return variety


class TargetListSerializer(serializers.ListSerializer):
    def to_internal_value(self, data):
        if not isinstance(data, list):
            return super().to_internal_value(data)

        errors = [{} for _ in data]
        relationship_fields = ("crop", "fieldbook", self.child.target_field_name)
        normalized_ids = {}
        resolved = {}
        for field_name in relationship_fields:
            related_field = self.child.fields[field_name]
            field_ids = {}
            for index, row in enumerate(data):
                if not isinstance(row, dict) or row.get(field_name) is None:
                    continue
                try:
                    field_ids[index] = related_field.normalize_pk(row[field_name])
                except serializers.ValidationError as exc:
                    errors[index][field_name] = exc.detail

            normalized_ids[field_name] = field_ids
            resolved[field_name] = related_field.get_queryset().filter(pk__in=set(field_ids.values())).in_bulk()

        prepared_data = []
        for index, row in enumerate(data):
            if not isinstance(row, dict):
                prepared_data.append(row)
                continue
            prepared_row = row.copy()
            for field_name in relationship_fields:
                if index not in normalized_ids[field_name]:
                    continue
                normalized_id = normalized_ids[field_name][index]
                if normalized_id not in resolved[field_name]:
                    related_field = self.child.fields[field_name]
                    try:
                        related_field.fail("does_not_exist", pk_value=normalized_id)
                    except serializers.ValidationError as exc:
                        errors[index][field_name] = exc.detail
                else:
                    prepared_row[field_name] = resolved[field_name][normalized_id]
            prepared_data.append(prepared_row)

        if any(errors):
            raise serializers.ValidationError(errors)
        return super().to_internal_value(prepared_data)

    def create(self, validated_data):
        plans = [self.child.build_plan(row, row_index=index) for index, row in enumerate(validated_data)]
        try:
            targets, created_count = create_targets(self.child.Meta.model, plans)
        except TargetPlanValidationError as exc:
            raise serializers.ValidationError(exc.errors) from exc
        self.created_count = created_count
        return targets


class BulkResolvedPrimaryKeyRelatedField(serializers.PrimaryKeyRelatedField):
    def normalize_pk(self, data):
        try:
            if self.pk_field is not None:
                return self.pk_field.to_internal_value(data)
            return self.queryset.model._meta.pk.to_python(data)
        except (TypeError, ValueError, DjangoValidationError):
            self.fail("incorrect_type", data_type=type(data).__name__)

    def to_internal_value(self, data):
        if isinstance(data, self.queryset.model):
            return data
        return super().to_internal_value(data)


class TargetSerializer(serializers.ModelSerializer):
    crop = BulkResolvedPrimaryKeyRelatedField(
        source="step.crop",
        queryset=Crop.objects.select_related("layout", "variety__species"),
    )
    fieldbook = BulkResolvedPrimaryKeyRelatedField(
        source="step.fieldbook",
        queryset=FieldBook.objects.select_related("layout"),
    )
    step = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        list_serializer_class = TargetListSerializer
        abstract = True

    def build_plan(self, attrs, row_index=0):
        field_name = self.target_field_name
        placement = attrs["step"]
        fieldbook = placement["fieldbook"]
        crop = placement["crop"]
        related_object = attrs[field_name]
        required_count = attrs.get("required_count", 1)
        return TargetPlan(fieldbook, crop, related_object, required_count, row_index)

    def validate(self, attrs):
        if isinstance(self.parent, serializers.ListSerializer):
            return attrs
        plan = self.build_plan(attrs)
        try:
            validate_target_identity(self.Meta.model, plan)
        except DjangoValidationError as exc:
            raise serializers.ValidationError(serializers.as_serializer_error(exc)) from exc
        return attrs

    def create(self, validated_data):
        try:
            targets, created_count = create_targets(self.Meta.model, [self.build_plan(validated_data)])
        except TargetPlanValidationError as exc:
            raise serializers.ValidationError(exc.errors[0]) from exc
        self.created_count = created_count
        return targets[0]


class TraitTargetSerializer(TargetSerializer):
    target_field_name = "trait"
    trait = BulkResolvedPrimaryKeyRelatedField(queryset=Trait.objects.select_related("protocol__plantspecies"))
    trait_numeric_id = serializers.IntegerField(source="trait.numeric_id", read_only=True)
    trait_description = serializers.CharField(source="trait.description", read_only=True)
    trait_display = serializers.StringRelatedField(source="trait", read_only=True)
    protocol = serializers.IntegerField(source="trait.protocol_id", read_only=True)
    protocol_name = serializers.CharField(source="trait.protocol.name", read_only=True)

    class Meta(TargetSerializer.Meta):
        model = TraitTarget
        fields = (
            "id",
            "crop",
            "fieldbook",
            "step",
            "trait",
            "trait_numeric_id",
            "trait_description",
            "trait_display",
            "protocol",
            "protocol_name",
            "required_count",
        )


class ParameterTargetSerializer(TargetSerializer):
    target_field_name = "parameter"
    parameter = BulkResolvedPrimaryKeyRelatedField(queryset=Parameter.objects.all())
    parameter_code = serializers.CharField(source="parameter.code", read_only=True)
    parameter_name = serializers.CharField(source="parameter.name", read_only=True)
    parameter_display = serializers.StringRelatedField(source="parameter", read_only=True)

    class Meta(TargetSerializer.Meta):
        model = ParameterTarget
        fields = (
            "id",
            "crop",
            "fieldbook",
            "step",
            "parameter",
            "parameter_code",
            "parameter_name",
            "parameter_display",
            "required_count",
        )
