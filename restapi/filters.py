import django_filters
from django_filters.rest_framework import FilterSet

from collect.models import Sample, SampleWeight, Storage, StoragePosition
from describe.models import Description, Protocol, Trait
from parameters.models import Parameter, VarietalParameter
from register.filters import filter_name_generic
from register.models import Entity, PlantSpecies, PlantVariety, Protection


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
        fields = (
            "name",
            "type",
            "country",
        )


class ProtectionFilter(FilterSet):
    class Meta:
        model = Protection
        fields = (
            "type",
            "reference",
            "status",
            "country",
            "variety",
            "applicants",
            "maintainers",
        )


class ProtocolFilter(FilterSet):
    variety = django_filters.NumberFilter(label="Variety", method="by_variety")

    class Meta:
        model = Protocol
        fields = ("name", "plantspecies")

    def by_variety(self, queryset, name, value):
        """Narrow protocols by a variety's species.

        This method is used by the description_create and
        description_update view to narrow the list of available
        protocols depending on the selected variety.

        FIXME: I don't like this. I'd rather rely on htmx to retrieve
        the updated select input instead of hitting the API.
        """
        variety = PlantVariety.objects.get(pk=value)
        return queryset.filter(plantspecies=variety.species)


class TraitFilter(FilterSet):
    class Meta:
        model = Trait
        fields = ("numeric_id", "protocol")


class DescriptionFilter(FilterSet):
    variety_name = django_filters.CharFilter(label="Variety Name", method="filter_variety_name")

    class Meta:
        model = Description
        fields = ("name", "protocol")

    def filter_variety_name(self, queryset, name, value):
        return filter_name_generic(queryset, "variety__name", value)


class StorageFilter(FilterSet):
    class Meta:
        model = Storage
        fields = {"name": ["exact", "icontains"]}


class StoragePositionFilter(FilterSet):
    class Meta:
        model = StoragePosition
        fields = ("name", "storage")


class SampleFilter(FilterSet):
    class Meta:
        model = Sample
        fields = ("sample_id", "variety", "notes", "growing_season", "position")


class SampleWeightFilter(FilterSet):
    class Meta:
        model = SampleWeight
        fields = ("sample", "weight")


class ParameterFilter(FilterSet):
    class Meta:
        model = Parameter
        fields = ("code",)


class VarietalParameterFilter(FilterSet):
    class Meta:
        model = VarietalParameter
        fields = ("parameter",)
