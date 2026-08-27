import django_filters
from django.db.models import Q
from django_filters import CharFilter, DateFilter, NumberFilter
from django_filters.rest_framework import DjangoFilterBackend, FilterSet

from calculator.models import ParameterObservation, TraitObservation
from collect.models import Germinability, Sample, SampleWeight, Storage, StoragePosition
from describe.models import Description, Expression, Protocol, State, Trait
from parameters.models import Parameter, VarietalParameter
from register.filters import filter_name_generic
from register.models import Entity, PlantSpecies, PlantVariety, Protection


class NoBrowsableAPIFilterBackend(DjangoFilterBackend):
    def to_html(self, request, queryset, view):
        return ""


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
    label = CharFilter(field_name="label__name", lookup_expr="iname")
    label__in = CharInFilter(field_name="label__name", lookup_expr="in")
    protocol__in = NumberInFilter(field_name="protocol", lookup_expr="in")
    variety_name = django_filters.CharFilter(label="Variety Name", method="filter_variety_name")
    variety__in = NumberInFilter(field_name="variety", lookup_expr="in")

    class Meta:
        model = Description
        fields = (
            "label",
            "label__in",
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


class ObservationFilter(FilterSet):
    crop__in = NumberInFilter(field_name="crop", lookup_expr="in")
    layout = NumberFilter(field_name="crop__layout")
    layout__in = NumberInFilter(field_name="crop__layout", lookup_expr="in")
    location = NumberFilter(field_name="crop__layout__location")
    location__in = NumberInFilter(field_name="crop__layout__location", lookup_expr="in")
    variety = NumberFilter(field_name="crop__variety")
    variety__in = NumberInFilter(field_name="crop__variety", lookup_expr="in")
    species = NumberFilter(field_name="crop__variety__species")
    species__in = NumberInFilter(field_name="crop__variety__species", lookup_expr="in")
    fieldbook_or_layout = CharFilter(method="filter_fieldbook_or_layout")
    recorded_at_start = DateFilter(field_name="recorded_at", lookup_expr="date__gte")
    recorded_at_end = DateFilter(field_name="recorded_at", lookup_expr="date__lte")

    def filter_fieldbook_or_layout(self, queryset, name, value):
        return queryset.filter(Q(crop__layout__name__icontains=value) | Q(step__fieldbook__name__icontains=value))

    class Meta:
        abstract = True


class TraitObservationFilter(ObservationFilter):
    state__in = NumberInFilter(field_name="state", lookup_expr="in")
    trait = NumberFilter(field_name="state__trait")
    trait__in = NumberInFilter(field_name="state__trait", lookup_expr="in")
    protocol = NumberFilter(field_name="state__trait__protocol")
    protocol__in = NumberInFilter(field_name="state__trait__protocol", lookup_expr="in")

    class Meta:
        model = TraitObservation
        fields = ("crop", "state")


class ParameterObservationFilter(ObservationFilter):
    parameter__in = NumberInFilter(field_name="parameter", lookup_expr="in")
    value = NumberFilter(field_name="parameter_value")
    value_min = NumberFilter(field_name="parameter_value", lookup_expr="gte")
    value_max = NumberFilter(field_name="parameter_value", lookup_expr="lte")
    parameter_date_start = DateFilter(field_name="parameter_date", lookup_expr="gte")
    parameter_date_end = DateFilter(field_name="parameter_date", lookup_expr="lte")

    class Meta:
        model = ParameterObservation
        fields = ("crop", "parameter", "parameter_value", "parameter_date")


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
