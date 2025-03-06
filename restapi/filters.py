import django_filters
from django_filters.rest_framework import FilterSet

from collect.models import SampleWeight, SeedSample, Storage, StoragePosition
from describe.models import Description, Protocol
from register.models import Entity, PlantSpecies, PlantVariety, Protection


class NumberInFilter(django_filters.BaseInFilter, django_filters.NumberFilter):
    pass


class PlantSpeciesFilter(FilterSet):
    class Meta:
        model = PlantSpecies
        fields = ("common_name", "latin_name", "plant_type")


class PlantVarietyFilter(FilterSet):
    class Meta:
        model = PlantVariety
        fields = ("name", "species")


class EntityFilter(FilterSet):
    class Meta:
        model = Entity
        fields = ("name",)


class ProtectionFilter(FilterSet):
    class Meta:
        model = Protection
        fields = ("variety", "type", "status", "reference")


class ProtocolFilter(FilterSet):
    variety = django_filters.NumberFilter(method="by_variety")

    class Meta:
        model = Protocol
        fields = ("name", "plantspecies")

    def by_variety(self, queryset, name, value):
        variety = PlantVariety.objects.get(pk=value)
        return queryset.filter(plantspecies=variety.species)


class DescriptionFilter(FilterSet):
    # FIXME: Is this really needed? Can't we just make multiple
    # requests instead of passing a list here?
    description = NumberInFilter(field_name="description", lookup_expr="in", label="Description IDs")
    variety = NumberInFilter(field_name="variety__pk", lookup_expr="in", label="Variety IDs")

    class Meta:
        model = Description
        fields = {"name": ["exact", "icontains"]}


class StorageFilter(FilterSet):
    class Meta:
        model = Storage
        fields = {"name": ["exact", "icontains"]}


class StoragePositionFilter(FilterSet):
    class Meta:
        model = StoragePosition
        fields = ("name", "storage")


class SeedSampleFilter(FilterSet):
    class Meta:
        model = SeedSample
        fields = ("sample_id", "variety", "notes", "growing_season", "position")


class SampleWeightFilter(FilterSet):
    class Meta:
        model = SampleWeight
        fields = ("seedsample", "weight")
