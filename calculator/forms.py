
from django import forms

from calculator.models import CropParameter

class CropParameterForm(forms.ModelForm):
    class Meta:
        model=CropParameter
        fields=('value',)
