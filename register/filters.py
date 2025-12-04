from crispy_forms.layout import Field, Layout, MultiWidgetField
from django import forms
from django.contrib.postgres.lookups import Unaccent
from django.contrib.postgres.search import TrigramSimilarity
from django.db.models import Case, F, IntegerField, Q, Value, When
from django.db.models.functions import Lower
from django_countries.fields import CountryField
from django_filters import (
    BooleanFilter,
    CharFilter,
    ChoiceFilter,
    Filter,
    FilterSet,
    ModelChoiceFilter,
    ModelMultipleChoiceFilter,
)

from frontpage.forms import HTMXFormMixin, SearchAndClearButtons
from frontpage.widgets import TomSelect, TomSelectMultiple
from register.models import (
    ENTITY_TYPE_CHOICES,
    PROTECTION_STATUS_CHOICES,
    PROTECTION_TYPE_CHOICES,
    Entity,
    PlantSpecies,
    PlantVariety,
)

TRIGRAM_SEARCH_THRESHOLD = 3


def filter_name_generic(queryset, field_name, value):
    if not value:
        return queryset

    search_expr = Lower(Unaccent(F(field_name)))

    qs = queryset.annotate(
        search_name=search_expr,
        similarity=TrigramSimilarity("search_name", value),
    )

    if len(value) < TRIGRAM_SEARCH_THRESHOLD:
        qs = qs.filter(search_name__icontains=value)
    else:
        qs = qs.filter(similarity__gt=0.1)

    qs = qs.annotate(
        rank=Case(
            When(search_name__iexact=value, then=Value(0)),
            When(search_name__istartswith=value, then=Value(1)),
            When(search_name__icontains=value, then=Value(2)),
            default=Value(3),
            output_field=IntegerField(),
        )
    )

    return qs.order_by("rank", "-similarity", "search_name")


class ProtectionFilterWidget(forms.MultiValueField):
    def __init__(self, *args, **kwargs):
        status_choices = PROTECTION_STATUS_CHOICES + [(None, "Any status")]
        type_choices = PROTECTION_TYPE_CHOICES + [(None, "Any type")]
        country_choices = CountryField().get_choices()
        fields = (
            forms.ChoiceField(choices=status_choices),
            forms.ChoiceField(choices=type_choices),
            forms.ChoiceField(choices=country_choices),
        )
        widget = forms.MultiWidget(
            widgets=[
                forms.Select(choices=status_choices),
                forms.Select(choices=type_choices),
                TomSelect(choices=country_choices),
            ]
        )
        super().__init__(fields=fields, widget=widget, **kwargs)

    def compress(self, data_list):
        if data_list:
            status, ptype, country = data_list
            return {"protection__status": status, "protection__type": ptype, "protection__country": country}
        return None


class ProtectionFilter(Filter):
    field_class = ProtectionFilterWidget

    def filter(self, qs, values):
        if values:
            # Ignore empty values
            filters = {k: v for k, v in values.items() if v}
            return qs.filter(**filters).distinct()
        return qs


class PlantVarietyFilterForm(HTMXFormMixin, forms.Form):
    hx_url: str = ""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper.form_method = "get"
        self.helper.layout = Layout(
            Field("name"),
            Field("species"),
            Field("has_descriptions"),
            Field("has_accessions"),
            MultiWidgetField("protection", attrs=({"class": "mt-1"})),
            SearchAndClearButtons(),
        )


class PlantSpeciesFilterForm(HTMXFormMixin, forms.Form):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper.layout = Layout(Field("common_name"), SearchAndClearButtons())


class PlantSpeciesFilter(FilterSet):
    common_name = CharFilter(label="Search", method="omni_search")

    class Meta:
        model = PlantSpecies
        fields = ("common_name",)
        form = PlantSpeciesFilterForm

    def omni_search(self, queryset, name, value):
        query = Q(common_name__icontains=value)
        query |= Q(latin_name__icontains=value)
        return queryset.filter(query)


class PlantVarietyFilter(FilterSet):
    name = CharFilter(label="Denomination", method="filter_name", field_name="names__name")
    species = ModelMultipleChoiceFilter(label="Species", queryset=PlantSpecies.objects.all(), widget=TomSelectMultiple)
    has_descriptions = BooleanFilter(label="Described", field_name="description", method="filter_has_records")
    has_accessions = BooleanFilter(label="Accession", field_name="sample", method="filter_has_records")
    protection = ProtectionFilter(label="Protection")

    class Meta:
        model = PlantVariety
        fields = ("name", "breeder")
        form = PlantVarietyFilterForm

    def filter_name(self, queryset, name, value):
        return filter_name_generic(queryset, name, value)

    def filter_has_records(self, queryset, name, value):
        lookup = f"{name}__isnull"
        if value is not None:
            return queryset.filter(**{lookup: not value}).distinct()
        return queryset


class EntityFilterForm(HTMXFormMixin, forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper.layout = Layout(Field("name"), Field("country"), Field("type"), SearchAndClearButtons())

    class Meta:
        model = Entity
        fields = ("name", "country", "type")


class EntityFilter(FilterSet):
    name = CharFilter(label="Name", method="filter_name", field_name="name")
    country = ChoiceFilter(choices=CountryField().get_choices(include_blank=False), widget=TomSelect)
    type = ChoiceFilter(choices=ENTITY_TYPE_CHOICES)

    def filter_name(self, queryset, name, value):
        return filter_name_generic(queryset, name, value)

    class Meta:
        form = EntityFilterForm


class ProtectionOmniFilterForm(HTMXFormMixin, forms.Form):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper.layout = Layout(
            Field("omni"),
            Field("variety__species"),
            Field("entities"),
            Field("type"),
            Field("status"),
            Field("country"),
            SearchAndClearButtons(),
        )


class ProtectionOmniFilter(FilterSet):
    omni = CharFilter(method="omni_search", label="Search")
    variety__species = ModelChoiceFilter(queryset=PlantSpecies.objects.all(), label="Species")
    entities = ModelChoiceFilter(
        queryset=Entity.objects.all(), label="Entity", widget=TomSelect, method="entity_search"
    )
    type = ChoiceFilter(choices=PROTECTION_TYPE_CHOICES)
    status = ChoiceFilter(choices=PROTECTION_STATUS_CHOICES)
    country = ChoiceFilter(choices=CountryField().get_choices(include_blank=False), widget=TomSelect)

    class Meta:
        form = ProtectionOmniFilterForm

    def omni_search(self, queryset, name, value):
        query = Q(variety__names__name__icontains=value)
        query |= Q(note__icontains=value)
        query |= Q(reference__icontains=value)
        return queryset.filter(query)

    def entity_search(self, queryset, name, value):
        query = Q()
        query |= Q(applicants=value)
        query |= Q(maintainers=value)
        return queryset.filter(query)
