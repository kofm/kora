import django_filters
from django_filters import CharFilter, NumberFilter
from django_filters.rest_framework import FilterSet

from collect.models import Germinability, Sample, SampleWeight, Storage, StoragePosition
from describe.models import Description, Expression, Protocol, State, Trait
from parameters.models import Parameter, VarietalParameter
from register.filters import filter_name_generic
from register.models import Entity, PlantSpecies, PlantVariety, Protection


class CharInFilter(django_filters.BaseInFilter, django_filters.CharFilter):
    pass


class NumberInFilter(django_filters.BaseInFilter, django_filters.NumberFilter):
    pass


class PlantSpeciesFilter(FilterSet):
    common_name__icontains = CharFilter(field_name="common_name", lookup_expr="icontains")
    latin_name__icontains = CharFilter(field_name="latin_name", lookup_expr="icontains")

    class Meta:
        model = PlantSpecies
        fields = (
            "common_name__icontains",
            "latin_name__icontains",
            "plant_type",
        )


class PlantVarietyFilter(FilterSet):
    id__in = NumberInFilter(field_name="pk", lookup_expr="in")
    name__in = CharInFilter(field_name="name", lookup_expr="in")
    name__icontains = CharFilter(field_name="name", lookup_expr="icontains")

    class Meta:
        model = PlantVariety
        fields = (
            "id__in",
            "name",
            "name__in",
            "name__icontains",
            "species",
        )


class EntityFilter(FilterSet):
    name__icontains = CharFilter(field_name="name", lookup_expr="icontains")

    class Meta:
        model = Entity
        fields = (
            "name",
            "name__icontains",
            "type",
            "country",
        )


class ProtectionFilter(FilterSet):
    reference__icontains = CharFilter(field_name="reference", lookup_expr="icontains")
    variety__in = NumberInFilter(field_name="variety", lookup_expr="in")

    class Meta:
        model = Protection
        fields = (
            "type",
            "reference",
            "reference__icontains",
            "status",
            "country",
            "variety",
            "applicants",
            "maintainers",
        )


class ProtocolFilter(FilterSet):
    exclude_id = NumberFilter(field_name="id", exclude=True)
    name__icontains = CharFilter(field_name="name", lookup_expr="icontains")
    plantspecies__in = NumberInFilter(field_name="plantspecies", lookup_expr="in")

    class Meta:
        model = Protocol
        fields = (
            "exclude_id",
            "name",
            "name__icontains",
            "plantspecies",
            "plantspecies__in",
        )


class TraitFilter(FilterSet):
    numeric_id__in = NumberInFilter(field_name="numeric_id", lookup_expr="in")
    protocol__in = NumberInFilter(field_name="protocol", lookup_expr="in")
    description__icontains = CharFilter(field_name="description", lookup_expr="icontains")

    class Meta:
        model = Trait
        fields = (
            "numeric_id",
            "numeric_id__in",
            "protocol",
            "protocol__in",
            "description__icontains",
        )


class StateFilter(FilterSet):
    trait__in = NumberInFilter(field_name="trait", lookup_expr="in")
    numeric_id__in = NumberInFilter(field_name="numeric_id", lookup_expr="in")
    description__icontains = CharFilter(field_name="description", lookup_expr="icontains")
    trait_numeric_id = NumberFilter(field_name="trait__numeric_id")
    trait_numeric_id__in = NumberInFilter(field_name="trait__numeric_id", lookup_expr="in")
    protocol = NumberFilter(field_name="trait__protocol_id")

    class Meta:
        model = State
        fields = (
            "trait",
            "trait__in",
            "numeric_id",
            "description__icontains",
        )


class DescriptionFilter(FilterSet):
    name__in = CharInFilter(field_name="name", lookup_expr="in")
    protocol__in = NumberInFilter(field_name="protocol", lookup_expr="in")
    variety_name = django_filters.CharFilter(label="Variety Name", method="filter_variety_name")
    variety__in = NumberInFilter(field_name="variety", lookup_expr="in")

    class Meta:
        model = Description
        fields = (
            "name",
            "name__in",
            "protocol",
            "protocol__in",
            "variety",
            "variety__in",
        )

    def filter_variety_name(self, queryset, name, value):
        return filter_name_generic(queryset, "variety__name", value)


class ExpressionFilter(FilterSet):
    description = NumberFilter(field_name="description")
    description__in = NumberInFilter(field_name="description", lookup_expr="in")
    state__in = NumberInFilter(field_name="state", lookup_expr="in")
    trait__in = NumberInFilter(field_name="state__trait", lookup_expr="in")
    trait_numeric_id = NumberFilter(field_name="state__trait__numeric_id")
    description_id__in = NumberInFilter(field_name="description_id", lookup_expr="in")
    note__icontains = CharFilter(field_name="note", lookup_expr="icontains")

    class Meta:
        model = Expression
        fields = (
            "description",
            "description__in",
            "trait__in",
            "trait_numeric_id",
            "state",
            "state__in",
            "note__icontains",
        )


class StorageFilter(FilterSet):
    class Meta:
        model = Storage
        fields = {"name": ["exact", "icontains"]}


class StoragePositionFilter(FilterSet):
    class Meta:
        model = StoragePosition
        fields = ("name", "storage")


class SampleFilter(FilterSet):
    sample_id__in = NumberInFilter(field_name="sample_id", lookup_expr="in")

    class Meta:
        model = Sample
        fields = ("sample_id", "variety", "notes", "growing_season", "position")


class SampleWeightFilter(FilterSet):
    sample__in = NumberInFilter(field_name="sample", lookup_expr="in")

    class Meta:
        model = SampleWeight
        fields = (
            "sample",
            "sample__in",
            "weight",
        )


class GerminabilityFilter(FilterSet):
    sample__in = NumberInFilter(field_name="sample", lookup_expr="in")

    class Meta:
        model = Germinability
        fields = ("sample", "sample__in")


class ParameterFilter(FilterSet):
    class Meta:
        model = Parameter
        fields = {"code": ["exact", "icontains"]}


class VarietalParameterFilter(FilterSet):
    variety__in = NumberInFilter(field_name="variety", lookup_expr="in")
    parameter_code = CharFilter("parameter__code")
    parameter_code__in = CharInFilter(field_name="parameter__code", lookup_expr="in")

    class Meta:
        model = VarietalParameter
        fields = (
            "variety",
            "parameter",
        )
