from django import forms
from django.core.exceptions import ValidationError
from django.db.models.base import Model
from django.forms.widgets import DateInput, HiddenInput, NumberInput
from django.shortcuts import get_object_or_404
from dynamic_forms import DynamicField, DynamicFormMixin

from calculator.models import Crop, CropParameter, Management
from calculator.utils import get_crop_params_list
from collect.models import CartItem


def get_form_initial_value(form: forms.Form, key: str) -> str:
    field = form.initial.get(key, None)
    # Sometimes a list is used instead of a single value
    return field[0] if isinstance(field, list) else field


def get_parameter_value(form: forms.Form) -> int | None:
    parameter = get_form_initial_value(form, "parameter")
    crop_id = get_form_initial_value(form, "crop")
    if parameter and crop_id:
        crop = get_object_or_404(Crop, pk=crop_id)
        cropparams = get_crop_params_list(crop)
        for param in filter(lambda x: x["parameter"] == int(parameter), cropparams):
            return param["value"]
    return None


class CropParameterForm(DynamicFormMixin, forms.ModelForm):
    class Meta:
        model = CropParameter
        fields = ("value", "parameter", "crop")
        widgets = {"crop": HiddenInput(), "value": NumberInput()}

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
        # initial = lambda form: form["parameter"].value(),
        initial=get_parameter_value,
        widget=lambda _: forms.TextInput(attrs={"class": "form-control my-3", "type": "numeric"}),
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
    # species = forms.CharField(label="Species")
    # variety = forms.CharField(label="Variety", required=False)
    sowing = forms.DateField(label="Sowing", required=False, widget=DateInput(attrs={"type": "date"}))
    harvest = forms.DateField(label="Harvest", required=False, widget=DateInput(attrs={"type": "date"}))

    class Meta:
        fields = ["species", "variety", "area", "notes"]
        model = Crop

    def has_changed(self) -> bool:
        return super().has_changed()

    def save(self):
        crop = super().save(commit=False)
        sowing = self.cleaned_data["sowing"]
        harvest = self.cleaned_data["harvest"]

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
                "Quantity retrieved cannot exceed the sample weight (" + self.instance.sample.variety.name + ")"
            )
        return cleaned_data
