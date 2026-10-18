from crispy_forms import layout
from django import forms
from django.db.models import Q
from django.urls import reverse_lazy
from django_filters import ChoiceFilter, FilterSet, ModelChoiceFilter, ModelMultipleChoiceFilter
from django_filters.filters import CharFilter

from frontpage.forms import HTMXFormMixin, SearchAndClearButtons, TomSelectModelFormMixin
from frontpage.widgets.tomselect import ModelTomSelect, ModelTomSelectMultiple, TomSelectConfig
from parameters.models import Parameter, VarietalParameter
from parameters.value_filters import TypedValueFilter
from register.models import PlantSpecies, PlantVariety


class ParameterFilterForm(HTMXFormMixin, forms.Form):
    name = forms.CharField()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper.layout = layout.Layout(
            layout.Field("search"),
            layout.Field("type"),
            layout.Div(
                layout.Submit("search", "Search", css_class="btn-sm"),
                layout.HTML('<a class="btn btn-sm btn-secondary" href=".">Clear</a>'),
                css_class="mt-0 mb-3",
            ),
        )


class ParameterFilter(FilterSet):
    search = CharFilter(label="Parameter", method="filter_name")
    type = ChoiceFilter(choices=Parameter.Type.choices)

    class Meta:
        model = Parameter
        fields = ("search", "type")
        form = ParameterFilterForm

    def filter_name(self, queryset, name, value):
        query = Q(code__icontains=value)
        query |= Q(name__icontains=value)
        query |= Q(description__icontains=value)
        return queryset.filter(query)


class VarietalParameterFilterForm(TomSelectModelFormMixin, HTMXFormMixin, forms.Form):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper.layout = layout.Layout(
            layout.Field("species"),
            layout.Field("variety"),
            layout.Field("parameter"),
            layout.Field("value_min"),
            layout.Field("value_max"),
            layout.Field("value_boolean"),
            layout.Field("value_text"),
            layout.Field("value_date_start"),
            layout.Field("value_date_end"),
            SearchAndClearButtons(),
        )


class VarietalParameterFilter(TypedValueFilter):
    species = ModelChoiceFilter(
        field_name="variety__species",
        queryset=PlantSpecies.objects.all(),
        widget=ModelTomSelect(
            ts_config=TomSelectConfig(
                url=reverse_lazy("register:plantspecies_autocomplete"),
                value_field="id",
                label_field="common_name",
                search_field=["common_name", "botanical_name"],
            )
        ),
        label="Species",
    )
    variety = ModelMultipleChoiceFilter(
        field_name="variety",
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
    parameter = ModelChoiceFilter(
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

    class Meta:
        fields = ()
        model = VarietalParameter
        form = VarietalParameterFilterForm
