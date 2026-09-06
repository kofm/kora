from crispy_forms.layout import Field, Layout
from django import forms
from django.db.models import Q
from django.urls import reverse_lazy
from django_filters import (
    CharFilter,
    ChoiceFilter,
    DateFilter,
    FilterSet,
    ModelChoiceFilter,
    ModelMultipleChoiceFilter,
    NumberFilter,
)

from calculator.models import CropLayout, FieldBook, ManagementType, ParameterObservation, TraitObservation
from describe.models import Protocol, Trait
from frontpage.forms import HTMXFormMixin, SearchAndClearButtons, TomSelectModelFormMixin
from frontpage.widgets import ModelTomSelect, ModelTomSelectMultiple, TomSelectConfig
from parameters.models import Parameter
from register.models import PlantSpecies, PlantVariety
from spaces.models import Location


class CropLayoutFilterForm(HTMXFormMixin, forms.Form):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper.layout = Layout(
            Field("name"),
            Field("location"),
            Field("status"),
            SearchAndClearButtons(),
        )


class CropLayoutFilter(FilterSet):
    name = CharFilter(lookup_expr="icontains", label="Name")
    location = ModelChoiceFilter(
        queryset=Location.objects.all(),
        widget=ModelTomSelect(
            ts_config=TomSelectConfig(
                url=reverse_lazy("spaces:location_autocomplete"),
                value_field="id",
                label_field="name",
                search_field="name",
            )
        ),
    )
    status = ChoiceFilter(
        method="filter_status",
        choices=(
            ("visible", "Visible"),
            ("archived", "Archived"),
            ("all", "All"),
        ),
        empty_label=None,
        label="Status",
    )

    def __init__(self, data=None, *args, **kwargs):
        if data is not None:
            data = data.copy()
            if not data.get("status"):
                data["status"] = "visible"
        super().__init__(data, *args, **kwargs)

    def filter_status(self, queryset, name, value):
        if value == "visible":
            return queryset.visible()
        if value == "archived":
            return queryset.archived()
        return queryset

    class Meta:
        model = CropLayout
        fields = ()
        form = CropLayoutFilterForm


class ManagementTypeFilterForm(HTMXFormMixin, forms.Form):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper.layout = Layout(
            Field("name"),
            SearchAndClearButtons(),
        )


class ManagementTypeFilter(FilterSet):
    name = CharFilter(lookup_expr="icontains", label="Name")

    class Meta:
        model = ManagementType
        fields = ()
        form = ManagementTypeFilterForm


class FieldBookFilterForm(HTMXFormMixin, forms.Form):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper.layout = Layout(
            Field("name"),
            Field("location"),
            SearchAndClearButtons(),
        )


class FieldBookFilter(FilterSet):
    name = CharFilter(lookup_expr="icontains", label="Name")
    location = ModelChoiceFilter(
        field_name="layout__location",
        queryset=Location.objects.all(),
        widget=ModelTomSelect(
            ts_config=TomSelectConfig(
                url=reverse_lazy("spaces:location_autocomplete"),
                value_field="id",
                label_field="name",
                search_field="name",
            )
        ),
    )

    class Meta:
        model = FieldBook
        fields = ()
        form = FieldBookFilterForm


class TraitObservationFilterForm(TomSelectModelFormMixin, HTMXFormMixin, forms.Form):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper.layout = Layout(
            Field("species"),
            Field("variety"),
            Field("location"),
            Field("fieldbook_or_layout"),
            Field("protocol"),
            Field("trait"),
            Field("recorded_at_start"),
            Field("recorded_at_end"),
            SearchAndClearButtons(),
        )


class TraitObservationFilter(FilterSet):
    species = ModelChoiceFilter(
        field_name="crop__variety__species",
        queryset=PlantSpecies.objects.all(),
        widget=ModelTomSelect(
            ts_config=TomSelectConfig(
                url=reverse_lazy("register:plantspecies_autocomplete"),
                value_field="id",
                label_field="common_name",
                search_field=["common_name", "latin_name"],
            )
        ),
        label="Species",
    )
    variety = ModelMultipleChoiceFilter(
        field_name="crop__variety",
        queryset=PlantVariety.objects.none(),
        widget=ModelTomSelectMultiple(
            ts_config=TomSelectConfig(
                url=reverse_lazy("register:variety_autocomplete"),
                value_field="id",
                label_field="name",
                search_field="name",
                depends_on="species",
                depends_param="species_id",
            )
        ),
        label="Variety",
    )
    location = ModelMultipleChoiceFilter(
        field_name="crop__layout__location",
        queryset=Location.objects.all(),
        widget=ModelTomSelectMultiple(
            ts_config=TomSelectConfig(
                url=reverse_lazy("spaces:location_autocomplete"),
                value_field="id",
                label_field="name",
                search_field="name",
            )
        ),
        label="Location",
    )
    fieldbook_or_layout = CharFilter(
        method="filter_fieldbook_or_layout",
        label="Field Book or Crop Layout",
    )
    protocol = ModelChoiceFilter(
        field_name="state__trait__protocol",
        queryset=Protocol.objects.all(),
        widget=ModelTomSelect(
            ts_config=TomSelectConfig(
                url=reverse_lazy("describe:protocol_autocomplete"),
                value_field="id",
                label_field="name",
                search_field="name",
            )
        ),
        label="Protocol",
    )
    trait = ModelChoiceFilter(
        field_name="state__trait",
        queryset=Trait.objects.none(),
        widget=ModelTomSelect(
            ts_config=TomSelectConfig(
                url=reverse_lazy("describe:trait_autocomplete"),
                value_field="id",
                label_field="text",
                search_field=["numeric_id", "description"],
                depends_on="protocol",
                depends_param="protocol_id",
            )
        ),
        label="Trait",
    )
    recorded_at_start = DateFilter(
        field_name="recorded_at",
        lookup_expr="date__gte",
        label="Recorded from",
        widget=forms.DateInput(attrs={"type": "date"}),
    )
    recorded_at_end = DateFilter(
        field_name="recorded_at",
        lookup_expr="date__lte",
        label="Recorded through",
        widget=forms.DateInput(attrs={"type": "date"}),
    )

    def filter_fieldbook_or_layout(self, queryset, name, value):
        return queryset.filter(Q(crop__layout__name__icontains=value) | Q(step__fieldbook__name__icontains=value))

    class Meta:
        model = TraitObservation
        fields = ()
        form = TraitObservationFilterForm


class ParameterObservationFilterForm(TomSelectModelFormMixin, HTMXFormMixin, forms.Form):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper.layout = Layout(
            Field("species"),
            Field("variety"),
            Field("location"),
            Field("fieldbook_or_layout"),
            Field("parameter"),
            Field("value_min"),
            Field("value_max"),
            Field("parameter_date_start"),
            Field("parameter_date_end"),
            Field("recorded_at_start"),
            Field("recorded_at_end"),
            SearchAndClearButtons(),
        )


class ParameterObservationFilter(FilterSet):
    species = ModelChoiceFilter(
        field_name="crop__variety__species",
        queryset=PlantSpecies.objects.all(),
        widget=ModelTomSelect(
            ts_config=TomSelectConfig(
                url=reverse_lazy("register:plantspecies_autocomplete"),
                value_field="id",
                label_field="common_name",
                search_field=["common_name", "latin_name"],
            )
        ),
        label="Species",
    )
    variety = ModelMultipleChoiceFilter(
        field_name="crop__variety",
        queryset=PlantVariety.objects.none(),
        widget=ModelTomSelectMultiple(
            ts_config=TomSelectConfig(
                url=reverse_lazy("register:variety_autocomplete"),
                value_field="id",
                label_field="name",
                search_field="name",
                depends_on="species",
                depends_param="species_id",
            )
        ),
        label="Variety",
    )
    location = ModelMultipleChoiceFilter(
        field_name="crop__layout__location",
        queryset=Location.objects.all(),
        widget=ModelTomSelectMultiple(
            ts_config=TomSelectConfig(
                url=reverse_lazy("spaces:location_autocomplete"),
                value_field="id",
                label_field="name",
                search_field="name",
            )
        ),
        label="Location",
    )
    fieldbook_or_layout = CharFilter(
        method="filter_fieldbook_or_layout",
        label="Field book or layout",
    )
    parameter = ModelChoiceFilter(
        field_name="parameter",
        queryset=Parameter.objects.all(),
        widget=ModelTomSelect(
            ts_config=TomSelectConfig(
                url=reverse_lazy("parameters:parameter_autocomplete"),
                value_field="id",
                label_field="text",
                search_field=["code", "name"],
            )
        ),
        label="Parameter",
    )
    value_min = NumberFilter(field_name="parameter_value", lookup_expr="gte", label="Value minimum")
    value_max = NumberFilter(field_name="parameter_value", lookup_expr="lte", label="Value maximum")
    parameter_date_start = DateFilter(
        field_name="parameter_date",
        lookup_expr="gte",
        label="Parameter date from",
        widget=forms.DateInput(attrs={"type": "date"}),
    )
    parameter_date_end = DateFilter(
        field_name="parameter_date",
        lookup_expr="lte",
        label="Parameter date through",
        widget=forms.DateInput(attrs={"type": "date"}),
    )
    recorded_at_start = DateFilter(
        field_name="recorded_at",
        lookup_expr="date__gte",
        label="Recorded from",
        widget=forms.DateInput(attrs={"type": "date"}),
    )
    recorded_at_end = DateFilter(
        field_name="recorded_at",
        lookup_expr="date__lte",
        label="Recorded through",
        widget=forms.DateInput(attrs={"type": "date"}),
    )

    def filter_fieldbook_or_layout(self, queryset, name, value):
        return queryset.filter(Q(crop__layout__name__icontains=value) | Q(step__fieldbook__name__icontains=value))

    class Meta:
        model = ParameterObservation
        fields = ()
        form = ParameterObservationFilterForm
