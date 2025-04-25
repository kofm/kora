from django import forms
from django.forms import widgets
from django_countries.fields import CountryField

from frontpage.widgets import TomSelect, TomSelectMultiple

from .models import PlantVariety, PlantVarietyName, Protection


class PlantVarietyForm(forms.ModelForm):
    class Meta:
        model = PlantVariety
        fields = ["name", "species", "breeder"]
        widgets = {"species": TomSelect, "breeder": TomSelect}


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
            "applicants": TomSelectMultiple,
            "maintainers": TomSelectMultiple,
            "date_start": widgets.DateInput(attrs={"type": "date"}),
            "date_end": widgets.DateInput(attrs={"type": "date"}),
        }
