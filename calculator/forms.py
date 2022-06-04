from django import forms
from django.core.exceptions import ValidationError
from django.db.models.base import Model
from django.forms.widgets import DateInput, HiddenInput
from django.shortcuts import get_object_or_404
from dynamic_forms import DynamicField, DynamicFormMixin

from calculator.models import Crop, CropParameter, Management
from calculator.utils import get_crop_params_list
from collect.models import CartItem


def get_form_initial_value(form, key):
    # Check if the key is present in the initial data dict
    if key in form.initial:
        # Data is returned in a list
        list_val = form[key].value()
        # Check if the list has exactly one item and use "sequence unpacking"
        # to retrieve the number. If list length is 0 or > 1 return None
        (val,) = list_val if len(list_val) == 1 else None
        return val
    # Return None by default
    return None


def get_parameter_value(form):
    if parameter := get_form_initial_value(form, "parameter"):
        crop = get_object_or_404(Crop, pk=get_form_initial_value(form, "crop"))
        cropparams = get_crop_params_list(crop)
        for param in filter(lambda x: x["parameter"] == int(parameter), cropparams):
            return param["value"]
    return None


class CropParameterForm(DynamicFormMixin, forms.ModelForm):
    class Meta:
        model = CropParameter
        fields = ("value", "parameter", "crop")
        widgets = {"crop": HiddenInput()}

    def save(self, commit: bool = ...) -> Model:
        parameter = self.cleaned_data["parameter"]
        value = self.cleaned_data["value"]
        crop = self.cleaned_data["crop"]
        _, cropparameter = CropParameter.objects.update_or_create(
            crop=crop, parameter=parameter, defaults={"value": value}
        )
        return cropparameter

    value = DynamicField(
        forms.CharField,
        required=False,
        # initial = lambda form: form["parameter"].value(),
        initial=get_parameter_value,
        widget=lambda _: forms.TextInput(
            attrs={"class": "form-control my-3", "type": "numeric"}
        ),
    )


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
