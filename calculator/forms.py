from django import forms
from django.core.exceptions import ValidationError
from django.forms.widgets import DateInput, HiddenInput

from calculator.models import CropParameter, Management
from collect.models import CartItem
from spaces.models import Area


class CropParameterForm(forms.ModelForm):
    class Meta:
        model = CropParameter
        fields = ("value",)


class ManagementForm(forms.ModelForm):
    class Meta:
        model = Management
        fields = [
            "type",
            "date",
            "notes",
        ]
        widgets = {"date": DateInput(attrs={"type": "date"})}


class CropManagementForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["date"].label = self.initial["type"].name

    class Meta:
        model = Management
        fields = ("date", "type")
        widgets = {
            "date": DateInput(
                attrs={
                    "type": "date",
                }
            ),
            "type": HiddenInput(),
        }


class CropForm(forms.Form):
    species = forms.CharField(label="Species")
    variety = forms.CharField(label="Variety", required=False)
    area = forms.ModelChoiceField(queryset=Area.objects.all())
    notes = forms.CharField(required=False)
    sowing = forms.DateField(
        label="Sowing", required=False, widget=DateInput(attrs={"type": "date"})
    )
    harvest = forms.DateField(
        label="Harvest", required=False, widget=DateInput(attrs={"type": "date"})
    )


class CartItemWeightForm(forms.ModelForm):
    class Meta:
        fields = ("weight",)
        model = CartItem

    def clean(self):
        cleaned_data = super().clean()
        weight = cleaned_data.get("weight")
        if weight > self.instance.sample.weight:
            raise ValidationError(
                "Quantity retrieved cannot exceed the sample weight ("
                + self.instance.sample.variety.name
                + ")"
            )
        return cleaned_data
