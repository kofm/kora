from django_filters import (
    BooleanFilter,
    CharFilter,
    ChoiceFilter,
    FilterSet,
)

from register.models import PlantVariety, Protection

PBR = "PBR"
NLI = "NLI"
CAT = "CAT"
PROTECTION_TYPE_CHOICES = [
    (PBR, "Plant Breeders' Right"),
    (NLI, "National Listing"),
    (CAT, "Common Catalogue"),
]
PROTECTION_STATUS_CHOICES = [
    ("G", "Granted"),
    ("T", "Terminated"),
    ("A", "Active Application"),
    ("W", "Withdrawn"),
    ("R", "Refused"),
]


class PlantVarietyFilter(FilterSet):
    name = CharFilter(
        label="Denomination", method="filter_name", field_name="names__name"
    )
    breeder = CharFilter(
        label="Breeder", method="filter_name", field_name="breeder__name"
    )
    has_descriptions = BooleanFilter(
        label="Described", field_name="description", method="filter_has_records",
    )
    has_accessions = BooleanFilter(
        label="Accession", field_name="seedsample", method="filter_has_records"
    )
    protection__type = ChoiceFilter(
        label="Protection", choices=PROTECTION_TYPE_CHOICES, null_label="None"
    )
    status = ChoiceFilter(
        label="Protection status",
        choices=PROTECTION_STATUS_CHOICES,
        method="filter_protection_status",
    )

    class Meta:
        model = PlantVariety
        fields = ("name", "breeder", "protection__type")
        sequence = (
            "name",
            "breeder",
            "has_descriptions",
            "has_accessions",
            "protection__type",
            "status",
        )

    def filter_name(self, queryset, name, value):
        lookup_icontains = "__".join([name, "icontains"])
        lookup_trigram = "__".join([name, "lower__trigram_similar"])
        if value:
            if len(value) < 3:
                queryset = queryset.filter(**{lookup_icontains: value})
            else:
                queryset = queryset.filter(**{lookup_trigram: value})
        return queryset

    def filter_has_records(self, queryset, name, value):
        lookup = "__".join([name, "isnull"])
        if value is not None:
            return queryset.filter(**{lookup: not value}).distinct()
        return queryset

    def filter_protection_status(self, queryset, name, value):
        protection_type = self.data.get("protection__type")
        if value is not None:
            protections = Protection.objects.filter(type=protection_type, status=value)
            return queryset.filter(protection__in=protections)
        return queryset
