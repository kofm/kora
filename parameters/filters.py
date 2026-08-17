from crispy_forms import layout
from django import forms
from django.db.models import Q
from django.urls import reverse_lazy
from django_filters import FilterSet, ModelChoiceFilter, ModelMultipleChoiceFilter, NumberFilter
from django_filters.filters import CharFilter

from frontpage.forms import HTMXFormMixin, SearchAndClearButtons, TomSelectModelFormMixin
from frontpage.widgets.tomselect import ModelTomSelect, ModelTomSelectMultiple, TomSelectConfig
from parameters.models import Parameter, VarietalParameter
from register.models import PlantSpecies, PlantVariety


class ParameterFilterForm(HTMXFormMixin, forms.Form):
    name = forms.CharField()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper.layout = layout.Layout(
            layout.Field("search"),
            layout.Div(
                layout.Submit("search", "Search", css_class="btn-sm"),
                layout.HTML('<a class="btn btn-sm btn-secondary" href=".">Clear</a>'),
                css_class="mt-0 mb-3",
            ),
        )


class ParameterFilter(FilterSet):
    search = CharFilter(label="Parameter", method="filter_name")

    class Meta:
        model = Parameter
        fields = ("search",)
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
            SearchAndClearButtons(),
        )


class VarietalParameterFilter(FilterSet):
    species = ModelChoiceFilter(
        field_name="variety__species",
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
    value_min = NumberFilter(field_name="value", lookup_expr="gte", label="Value minimum")
    value_max = NumberFilter(field_name="value", lookup_expr="lte", label="Value maximum")

    class Meta:
        fields = ()
        model = VarietalParameter
        form = VarietalParameterFilterForm
