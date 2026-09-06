from numbers import Integral, Real

from django.db.models import Count, Q
from rest_framework import serializers as sr

from describe.models import Description, DescriptionLabel, Protocol, State, Trait
from register.models import PlantVariety
from restapi.fields import QueryField
from restapi.serializers.generic import (
    BaseSpreadsheetImportRequestSerializer,
    build_bulk_lookup_map,
)


def parse_numeric_id(value):
    """Parse a spreadsheet numeric id, given as int, float, or string."""
    if isinstance(value, bool):
        return None
    if isinstance(value, Integral):
        return int(value)
    if isinstance(value, Real):
        return int(value) if float(value).is_integer() else None
    try:
        return int(str(value).strip())
    except (TypeError, ValueError):
        return None


class TraitValuesField(sr.Field):
    """Parse the dynamic wide trait columns of a single row.

    Receives the raw ``{trait_numeric_id: cell_value}`` mapping for the
    trait columns present in the row and returns the list of matching
    ``State`` objects. Trait and state numeric ids are validated against
    the protocol.
    """

    def to_internal_value(self, data):
        if not data:
            return []
        state_map = self.context["state_map"]
        trait_numeric_ids = self.context["trait_numeric_ids"]

        errors = []
        states = []
        for trait_id, value in data.items():
            if trait_id not in trait_numeric_ids:
                errors.append(f"Trait with numeric id {trait_id} is not part of the protocol.")
                continue
            state_id = parse_numeric_id(value)
            if state_id is None:
                errors.append(f"Trait {trait_id}: value {value!r} is not numeric.")
                continue
            state = state_map.get((trait_id, state_id))
            if state is None:
                errors.append(f"Trait {trait_id}: state numeric id {state_id} is not valid for this trait.")
                continue
            states.append(state)
        if errors:
            raise sr.ValidationError(errors)
        return states


class DescriptionImportListSerializer(sr.ListSerializer):
    def _ambiguous_variety_names(self, queryset, data):
        names = {row.get("variety_name") for row in data if row.get("variety_name")}
        if not names:
            return set()
        return set(
            queryset.filter(name__in=names)
            .values("name")
            .annotate(count=Count("id"))
            .filter(count__gt=1)
            .values_list("name", flat=True)
        )

    def _extra_errors(self, data):
        """Row-level errors that are not expressible as single-field errors."""
        errors = [{} for _ in data]
        ambiguous = self.context.get("ambiguous_varieties", set())
        label_map = self.context.get("label_map", {})

        seen = {}
        for index, row in enumerate(data):
            variety_name = row.get("variety_name")
            if variety_name in ambiguous:
                errors[index]["variety"] = [
                    f"Multiple varieties match the name {variety_name!r} for the protocol species."
                ]
            label_name = row.get("label_name")
            if label_name and (label_name,) not in label_map:
                errors[index]["label"] = [f"Description label {label_name!r} does not exist."]

            if variety_name is None:
                continue
            key = (variety_name, label_name)
            if key in seen:
                message = f"Duplicate row for variety {variety_name!r} and label {label_name!r}."
                errors[index]["non_field_errors"] = [message]
                errors[seen[key]]["non_field_errors"] = [message]
            else:
                seen[key] = index
        return errors

    def to_internal_value(self, data):
        protocol = self.context["protocol"]

        variety_queryset = PlantVariety.objects.filter(species=protocol.plantspecies)
        self.context["variety_map"] = build_bulk_lookup_map(
            variety_queryset,
            {"variety_name": "name"},
            data,
        )
        self.context["ambiguous_varieties"] = self._ambiguous_variety_names(variety_queryset, data)
        self.context["label_map"] = build_bulk_lookup_map(
            DescriptionLabel.objects.all(),
            {"label_name": "name"},
            data,
        )
        states = State.objects.filter(trait__protocol=protocol).select_related("trait")
        self.context["state_map"] = {(state.trait.numeric_id, state.numeric_id): state for state in states}
        self.context["trait_numeric_ids"] = set(
            Trait.objects.filter(protocol=protocol).values_list("numeric_id", flat=True)
        )

        extra_errors = self._extra_errors(data)
        try:
            validated = super().to_internal_value(data)
        except sr.ValidationError as exc:
            details = list(exc.detail)
            merged = [{**detail, **extra} for detail, extra in zip(details, extra_errors, strict=True)]
            raise sr.ValidationError(merged) from exc

        if any(extra_errors):
            raise sr.ValidationError(extra_errors)
        return validated

    def create(self, validated_data):
        protocol = self.context["protocol"]

        pairs = {(item["variety"], item.get("label")) for item in validated_data}
        existing_keys = set()
        if pairs:
            query = Q()
            for variety, label in pairs:
                query |= Q(variety=variety, protocol=protocol, label=label)
            existing_keys = set(Description.objects.filter(query).values_list("variety_id", "label_id"))

        results = []
        for item in validated_data:
            variety = item.get("variety")
            label = item.get("label")
            if variety is None:
                continue
            key = (variety.pk, label.pk if label else None)
            if key in existing_keys:
                continue
            description = Description(
                protocol=protocol,
                variety=variety,
                label=label,
                notes=item.get("notes", ""),
            )
            results.append((description, item.get("trait_values", [])))
        return results


class DescriptionImportRowSerializer(sr.Serializer):
    variety = QueryField(
        mapping_key="variety_map",
        column_mapping={"variety_name": "name"},
        required=True,
    )
    label = QueryField(
        mapping_key="label_map",
        column_mapping={"label_name": "name"},
        required=False,
    )
    notes = sr.CharField(required=False, allow_blank=True, max_length=500)
    trait_values = TraitValuesField(required=False)

    class Meta:
        list_serializer_class = DescriptionImportListSerializer


class DescriptionImportRequestSerializer(BaseSpreadsheetImportRequestSerializer):
    protocol_id = sr.PrimaryKeyRelatedField(queryset=Protocol.objects.all(), required=True)

    row_serializer = DescriptionImportRowSerializer

    def validate(self, attrs):
        attrs = super().validate(attrs)

        rows = []
        for row in attrs["_rows"]:
            reshaped = {key: value for key, value in row.items() if key in ("variety_name", "label_name", "notes")}
            reshaped["trait_values"] = {
                trait_id: value for key, value in row.items() if (trait_id := parse_numeric_id(key)) is not None
            }
            rows.append(reshaped)
        attrs["_rows"] = rows
        return attrs

    def create(self, validated_data):
        rows = validated_data.pop("_rows", [])
        protocol = validated_data.pop("protocol_id")
        validate_only = validated_data.get("validate_only")

        row_serializer = self.row_serializer(data=rows, many=True, context={"protocol": protocol})
        row_serializer.is_valid(raise_exception=True)
        if validate_only:
            return []
        return row_serializer.save()
