from django import forms
from django.urls import reverse_lazy

from frontpage.forms import TomSelectModelFormMixin
from frontpage.widgets import ModelTomSelect, TomSelectConfig
from register.models import PlantSpecies, PlantVariety

from .models import Parameter, VarietalParameter
from .value_forms import TypedValueFormMixin
from .values import VALUE_FIELDS


class ParameterForm(forms.ModelForm):
    class Meta:
        model = Parameter
        fields = ("code", "name", "description", "type", "measure_unit")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if not self.instance._state.adding:
            self.fields["type"].disabled = True


class VarietalParameterForm(TypedValueFormMixin, TomSelectModelFormMixin, forms.ModelForm):
    species = forms.ModelChoiceField(
        queryset=PlantSpecies.objects.all(),
        widget=ModelTomSelect(
            ts_config=TomSelectConfig(
                url=reverse_lazy("register:plantspecies_autocomplete"),
                value_field="id",
                label_field="common_name",
                search_field=["common_name", "botanical_name"],
            )
        ),
    )
    variety = forms.ModelChoiceField(
        queryset=PlantVariety.objects.none(),
        widget=ModelTomSelect(
            ts_config=TomSelectConfig(
                url=reverse_lazy("register:variety_autocomplete"),
                value_field="id",
                label_field="name",
                search_field="name",
                depends_on="species",
                depends_param="species_id",
            )
        ),
    )
    parameter = forms.ModelChoiceField(
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
        model = VarietalParameter
        fields = ("species", "variety", "parameter", *VALUE_FIELDS, "note", "url_ref")
        labels = {"url_ref": "URL"}


class VarietalParameterUpdateForm(TypedValueFormMixin, forms.ModelForm):
    class Meta:
        model = VarietalParameter
        fields = (*VALUE_FIELDS, "note", "url_ref")
        labels = {"url_ref": "URL"}


class VarietyVarietalParameterForm(TypedValueFormMixin, forms.ModelForm):
    parameter = forms.ModelChoiceField(
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
        model = VarietalParameter
        fields = ("parameter", *VALUE_FIELDS, "note", "url_ref")
        labels = {"url_ref": "URL"}
