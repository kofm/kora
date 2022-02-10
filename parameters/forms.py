from django.forms import ModelForm
from django.forms.widgets import HiddenInput
from .models import CropParameter, VarietalParameter

class CropParameterForm(ModelForm):
    class Meta:
        model = CropParameter
        fields = '__all__'
        widgets = {'specie': HiddenInput()}


class VarietalParameterForm(ModelForm):
    class Meta:
        model = VarietalParameter
        fields = '__all__'
        widgets = {'variety': HiddenInput()}
