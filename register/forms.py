from django import forms
from django.forms import ModelChoiceField, widgets
from django.urls import reverse_lazy
from django_countries.fields import CountryField

from frontpage.widgets import ModelTomSelect, ModelTomSelectMultiple, TomSelect, TomSelectConfig

from .models import Entity, PlantSpecies, PlantVariety, PlantVarietyName, Protection, ProtectionType


class PlantVarietyForm(forms.ModelForm):
    species = ModelChoiceField(
        queryset=PlantSpecies.objects.all(),
        widget=ModelTomSelect(
            ts_config=TomSelectConfig(
                url=reverse_lazy("register:plantspecies_autocomplete"),
                value_field="id",
                label_field="common_name",
                search_field=["common_name", "latin_name"],
            )
        ),
    )

    class Meta:
        model = PlantVariety
        fields = ["name", "species"]


class PlantVarietyNameForm(forms.ModelForm):
    class Meta:
        model = PlantVarietyName
        fields = ["name", "change_date"]


class ProtectionForm(forms.ModelForm):
    country = CountryField(blank=True).formfield(widget=TomSelect)

    class Meta:
        model = Protection

        fields = (
            "type",
            "status",
            "country",
            "reference",
            "applicants",
            "maintainers",
            "date_start",
            "date_end",
            "note",
        )
        widgets = {
            "country": TomSelect,
            "applicants": ModelTomSelectMultiple(
                ts_config=TomSelectConfig(
                    url=reverse_lazy("register:entity_autocomplete"),
                    value_field="id",
                    label_field="name",
                    search_field="name",
                )
            ),
            "maintainers": ModelTomSelectMultiple(
                ts_config=TomSelectConfig(
                    url=reverse_lazy("register:entity_autocomplete"),
                    value_field="id",
                    label_field="name",
                    search_field="name",
                )
            ),
            "date_start": widgets.DateInput(attrs={"type": "date"}),
            "date_end": widgets.DateInput(attrs={"type": "date"}),
        }


class ProtectionTypeForm(forms.ModelForm):
    class Meta:
        model = ProtectionType
        fields = ("name", "code")

    def clean_code(self):
        return self.cleaned_data["code"].strip().upper()


class EntityForm(forms.ModelForm):
    country = CountryField(blank=True).formfield(widget=TomSelect)

    class Meta:
        model = Entity
        fields = ("name", "type", "country", "contact", "email")
