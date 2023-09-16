from django.db.models import Q
from django_countries.fields import CountryField
from django_filters import (
    BooleanFilter,
    CharFilter,
    Filter,
    FilterSet,
)
from django import forms

from register.models import PlantVariety

PBR = "PBR"
NLI = "NLI"
CAT = "CAT"

PROTECTION_TYPE_CHOICES = [
    (None, "Any type"),
    (PBR, "Plant Breeders' Right"),
    (NLI, "National Listing"),
    (CAT, "Common Catalogue"),
]

PROTECTION_STATUS_CHOICES = [
    (None, "Any status"),
    ("G", "Granted"),
    ("T", "Terminated"),
    ("A", "Active Application"),
    ("W", "Withdrawn"),
    ("R", "Refused"),
    ("S", "Surrendered"),
]


def filter_name_generic(queryset, name, value):
    lookup_icontains = "__".join([name, "unaccent__icontains"])
    lookup_trigram = "__".join([name, "unaccent__lower__trigram_similar"])
    if value:
        if len(value) < 7:
            queryset = queryset.filter(**{lookup_icontains: value})
        else:
            queryset = queryset.filter(**{lookup_trigram: value})
    return queryset


class ProtectionFilterWidget(forms.MultiValueField):
    def __init__(self, *args, **kwargs):
        fields = (
            forms.ChoiceField(choices=PROTECTION_STATUS_CHOICES),
            forms.ChoiceField(choices=PROTECTION_TYPE_CHOICES),
            forms.ChoiceField(choices=CountryField().get_choices()),
        )
        widget = forms.MultiWidget(
            widgets=[
                forms.Select(choices=PROTECTION_STATUS_CHOICES),
                forms.Select(attrs={"class": "mt-1"}, choices=PROTECTION_TYPE_CHOICES),
                forms.Select(attrs={"class": "mt-1"}, choices=CountryField().get_choices()),
            ]
        )
        super().__init__(fields=fields, widget=widget, *args, **kwargs)

    def compress(self, data_list):
        if data_list:
            return {
                "protection__status": data_list[0],
                "protection__type": data_list[1],
                "protection__country": data_list[2],
            }
        return None


class ProtectionFilter(Filter):
    field_class = ProtectionFilterWidget

    def filter(self, qs, values):
        print(values)
        if values:
            filters = {k: v for k, v in values.items() if v != ""}
            return qs.filter(**filters).distinct()
        return qs


class PlantVarietyFilter(FilterSet):
    name = CharFilter(
        label="Denomination", method="filter_name", field_name="names__name"
    )
    breeder = CharFilter(
        label="Breeder", method="filter_name", field_name="breeder__name"
    )
    has_descriptions = BooleanFilter(
        label="Described",
        field_name="description",
        method="filter_has_records",
    )
    has_accessions = BooleanFilter(
        label="Accession", field_name="seedsample", method="filter_has_records"
    )
    protection = ProtectionFilter(label="Protection")

    class Meta:
        model = PlantVariety
        fields = (
            "name",
            "breeder",
        )

    def filter_name(self, queryset, name, value):
        return filter_name_generic(queryset, name, value)

    def filter_has_records(self, queryset, name, value):
        lookup = "__".join([name, "isnull"])
        if value is not None:
            return queryset.filter(**{lookup: not value}).distinct()
        return queryset


class EntityFilter(FilterSet):
    name = CharFilter(label="Name", method="filter_name", field_name="name")

    def filter_name(self, queryset, name, value):
        return filter_name_generic(queryset, name, value)
