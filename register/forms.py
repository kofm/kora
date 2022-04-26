from django import forms
from django.forms import widgets

from .models import PlantSpecies, PlantVariety, PlantVarietyName


class PlantSpeciesForm(forms.ModelForm):
    class Meta:
        model = PlantSpecies
        fields = ["common_name", "latin_name", "plant_type"]
        widgets = {"common_name": forms.TextInput(attrs={"class": "form-control"})}


class PlantVarietyForm(forms.ModelForm):
    class Meta:
        model = PlantVariety
        fields = ['name', 'species', ]
        widgets = {"species": forms.HiddenInput()}

class PlantVarietyNameForm(forms.ModelForm):
    class Meta:
        model = PlantVarietyName
        fields = ['name', ]
