from django import forms
from django.forms import widgets
from django_countries.fields import CountryField

from .models import PlantVariety, PlantVarietyName, Protection


class PlantVarietyForm(forms.ModelForm):
    class Meta:
        model = PlantVariety
        fields = ["name", "species", "breeder"]


class PlantVarietyNameForm(forms.ModelForm):
    class Meta:
        model = PlantVarietyName
        fields = ["name"]


class ProtectionForm(forms.ModelForm):
    country = CountryField(blank=True).formfield()

    class Meta:
        model = Protection
        exclude = ("variety",)
        widgets = {
            "date_start": widgets.DateInput(attrs={"type": "date"}),
            "date_end": widgets.DateInput(attrs={"type": "date"}),
        }
