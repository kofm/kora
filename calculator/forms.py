from django import forms
from django.core.exceptions import ValidationError
from django.db.models.base import Model
from django.forms.widgets import DateInput, HiddenInput

from calculator.models import Crop, CropParameter, Management
from collect.models import CartItem


class CropParameterForm(forms.ModelForm):
    class Meta:
        model = CropParameter
        fields = ("value", "parameter", "crop")
        widgets = {"crop": HiddenInput()}

    def save(self, commit: bool = ...) -> Model:
        parameter = self.cleaned_data["parameter"]
        value = self.cleaned_data["value"]
        crop = self.cleaned_data["crop"]
        created, cropparameter = CropParameter.objects.update_or_create(
            crop=crop, parameter=parameter, defaults={"value": value}
        )
        return cropparameter



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


class CropModelForm(forms.ModelForm):
    species = forms.CharField(label="Species")
    variety = forms.CharField(label="Variety", required=False)
    sowing = forms.DateField(
        label="Sowing", required=False, widget=DateInput(attrs={"type": "date"})
    )
    harvest = forms.DateField(
        label="Harvest", required=False, widget=DateInput(attrs={"type": "date"})
    )

    class Meta:
        fields = ["area", "notes"]
        model = Crop

    def save(self, commit=True):
        crop = super().save(commit=False)
        variety = self.cleaned_data["variety"]
        species = self.cleaned_data["species"]
        sowing = self.cleaned_data["sowing"]
        harvest = self.cleaned_data["harvest"]

        if variety:
            crop.set_crop(variety, "plantvariety")
        else:
            crop.set_crop(species, "plantspecies")

        crop.save()

        if sowing:
            crop.sowing = sowing
        elif crop.sowing:
            del crop.sowing
        if harvest:
            crop.harvest = harvest
        elif crop.harvest:
            del crop.harvest
        return crop


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
