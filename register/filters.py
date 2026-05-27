from crispy_forms.bootstrap import InlineField
from crispy_forms.layout import Field, Layout, MultiWidgetField
from django import forms
from django.contrib.postgres.lookups import Unaccent
from django.contrib.postgres.search import TrigramSimilarity
from django.db.models import (
    BLANK_CHOICE_DASH,
    Case,
    CharField,
    Exists,
    F,
    FloatField,
    IntegerField,
    OuterRef,
    Q,
    Subquery,
    Value,
    When,
)
from django.db.models.functions import Lower
from django.forms import ChoiceField
from django.urls import reverse_lazy
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

from collect.models import Sample
from describe.models import Description, DescriptionLabel
from describe.widgets import DescriptionLabelSelectMultiple
from frontpage.forms import HTMXFormMixin, SearchAndClearButtons
from frontpage.widgets import ModelTomSelect, ModelTomSelectMultiple, TomSelect, TomSelectConfig
from register.models import (
    ENTITY_TYPE_CHOICES,
    PROTECTION_STATUS_CHOICES,
    Entity,
    PlantSpecies,
    PlantVariety,
    PlantVarietyName,
    Protection,
    ProtectionType,
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


def ranked_plantvarietyname_subquery(value):
    value = value.strip().lower()

    search_expr = Lower(Unaccent("name"))

    qs = PlantVarietyName.objects.filter(
        variety_id=OuterRef("pk"),
    ).annotate(
        search_name=search_expr,
        similarity=TrigramSimilarity(search_expr, value),
    )

    if len(value) < TRIGRAM_SEARCH_THRESHOLD:
        qs = qs.filter(search_name__istartswith=value)
    else:
        qs = qs.filter(similarity__gt=0.1)

    return qs.annotate(
        rank=Case(
            When(search_name__iexact=value, then=Value(0)),
            When(search_name__istartswith=value, then=Value(1)),
            When(search_name__icontains=value, then=Value(2)),
            default=Value(3),
            output_field=IntegerField(),
        )
    ).order_by("rank", "-similarity", "search_name")


class ProtectionFilterField(forms.MultiValueField):
    def __init__(self, *args, **kwargs):
        status_choices = PROTECTION_STATUS_CHOICES + BLANK_CHOICE_DASH
        status_field = forms.ChoiceField(choices=status_choices)
        type_field = forms.ModelChoiceField(queryset=ProtectionType.objects.all())
        country_choices = CountryField().get_choices()
        country_field = forms.ChoiceField(choices=country_choices)

        fields = (status_field, type_field, country_field)
        widget = forms.MultiWidget(
            widgets=[
                forms.Select(choices=status_choices),
                forms.Select(choices=type_field.choices),
                TomSelect(choices=country_choices),
            ]
        )
        super().__init__(fields=fields, widget=widget, **kwargs)

    def compress(self, data_list):
        if data_list:
            status, ptype, country = data_list
            return {"status": status, "type": ptype, "country": country}
        return None


class ProtectionFilter(Filter):
    field_class = ProtectionFilterField

    def filter(self, qs, value):
        if value:
            # Ignore empty values
            filters = {k: v for k, v in value.items() if v}
            protections = Protection.objects.filter(variety=OuterRef("pk"), **filters)
            return qs.filter(Exists(protections))
        return qs


class PlantVarietyFilterForm(HTMXFormMixin, forms.Form):
    hx_url: str = ""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper.form_method = "get"
        self.helper.form_id = "variety-filter"
        self.helper.attrs.update({"hx_include": "#id_order"})
        self.helper.layout = Layout(
            Field("name"),
            Field("species"),
            Field("description"),
            Field("description_label"),
            Field("sample"),
            MultiWidgetField("protection", attrs=({"class": "mt-1"})),
            SearchAndClearButtons(),
        )


class PlantVarietyCardsOrderForm(HTMXFormMixin, forms.Form):
    ORDER_CHOICES = [
        ("created_at:desc", "Created (desc)"),
        ("created_at:asc", "Created (asc)"),
        ("name:asc", "Name (asc)"),
        ("name:desc", "Name (desc)"),
    ]
    order = ChoiceField(choices=ORDER_CHOICES, required=False)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper.form_class = "form-inline"
        self.helper.field_template = "bootstrap5/layout/inline_field.html"
        self.helper.attrs.update({"hx_target": "#results", "hx_include": "#variety-filter"})
        self.helper.layout = Layout(InlineField("order", css_class="form-select"))

    def save(self):
        order = self.cleaned_data["order"]
        if not order:
            return "-created_at"
        ordering, direction = order.split(":")
        if direction == "desc":
            ordering = f"-{ordering}"
        return ordering


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
    species = ModelMultipleChoiceFilter(
        queryset=PlantSpecies.objects.all(),
        widget=ModelTomSelectMultiple(
            ts_config=TomSelectConfig(
                url=reverse_lazy("register:plantspecies_autocomplete"),
                search_param="common_name__icontains",
                value_field="id",
                label_field="common_name",
                search_field=["common_name", "latin_name"],
                preload="true",
            )
        ),
        label="Species",
    )
    description = BooleanFilter(label="Described", field_name="description", method="filter_description")
    description_label = ModelMultipleChoiceFilter(
        label="Description Label",
        queryset=DescriptionLabel.objects.all(),
        widget=DescriptionLabelSelectMultiple,
        method="filter_description_label",
    )
    sample = BooleanFilter(label="Sample", field_name="sample", method="filter_sample")
    protection = ProtectionFilter(label="Protection")

    class Meta:
        model = PlantVariety
        fields = ("name", "breeder")
        form = PlantVarietyFilterForm

    def filter_name(self, queryset, name, value):
        if not value:
            return queryset

        name_subquery = ranked_plantvarietyname_subquery(value)
        name_rank = Subquery(name_subquery.values("rank")[:1], output_field=IntegerField())
        name_similarity = Subquery(name_subquery.values("similarity")[:1], output_field=FloatField())
        search_name = Subquery(name_subquery.values("search_name")[:1], output_field=CharField())
        return (
            queryset.filter(Exists(name_subquery))
            .alias(name_rank=name_rank, name_similarity=name_similarity, search_name=search_name)
            .order_by("name_rank", "-name_similarity", "search_name")
        )

    def filter_description(self, queryset, name, value):
        if value == "":
            return queryset

        has_description = Exists(Description.objects.filter(variety=OuterRef("pk")))

        return queryset.filter(has_description if value else ~has_description)

    def filter_description_label(self, queryset, name, value):
        if not value:
            return queryset
        desc = Exists(Description.objects.filter(variety=OuterRef("pk"), label__in=value))
        return queryset.filter(desc)

    def filter_sample(self, queryset, name, value):
        if value == "":
            return queryset
        samp = Exists(Sample.objects.filter(variety=OuterRef("pk")))
        return queryset.filter(samp if value else ~samp)


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
        queryset=Entity.objects.all(),
        label="Entity",
        widget=ModelTomSelect(
            ts_config=TomSelectConfig(
                url=reverse_lazy("register:entity_autocomplete"),
                value_field="id",
                label_field="name",
                search_field="name",
            )
        ),
        method="entity_search",
    )
    type = ModelChoiceFilter(queryset=ProtectionType.objects.all(), label="Type")
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
