from django.forms import ModelForm
from django.forms.widgets import HiddenInput

from .models import SpeciesParameter, VarietalParameter


class SpeciesParameterForm(ModelForm):
    class Meta:
        model = SpeciesParameter
        fields = "__all__"
        widgets = {"specie": HiddenInput()}


class VarietalParameterForm(ModelForm):
    class Meta:
        model = VarietalParameter
        fields = "__all__"
        widgets = {"variety": HiddenInput()}
