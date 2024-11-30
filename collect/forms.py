from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit

from collect.models import (
    Cart,
    CartItem,
    Germinability,
    SampleWeight,
    SeedSample,
    Storage,
    StoragePosition,
)
from django import forms
from django.core.validators import MinValueValidator
from django.db import transaction
from django.forms.widgets import HiddenInput
from django.shortcuts import get_object_or_404


class SeedSampleForm(forms.ModelForm):
    tomvar = forms.CharField(label="Variety")
    tompos = forms.CharField(label="Position")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.layout = Layout(
            "tomvar",
            "variety",
            "sample_id",
            "tompos",
            "position",
            "growing_season",
            "notes",
        )

    class Meta:
        model = SeedSample
        fields = (
            "sample_id",
            "tomvar",
            "variety",
            "tompos",
            "position",
            "growing_season",
            "notes",
        )
        widgets = {
            "variety": HiddenInput(),
            "position": HiddenInput(),
        }


class SampleWeightForm(forms.ModelForm):
    class Meta:
        model = SampleWeight
        fields = ("weight",)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.add_input(Submit("submit", "Submit", css_class="col-12 mt-3"))


class GerminabilityForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["germinability"].required = False

    class Meta:
        model = Germinability
        fields = ("germinability", "after_days", "performed_at")


class SeedSampleYearForm(forms.Form):
    year = forms.ChoiceField(
        choices=((0, ""),),
        widget=forms.Select(
            attrs={
                "class": "form-select",
                "hx-get": "_hx",
                "hx-trigger": "change",
                "hx-target": "#seedsample-table",
                "hx-include": "#search-form",
            }
        ),
    )


class CartSelectForm(forms.Form):
    def __init__(self, *args, user=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["cart"].empty_label = None
        self.fields["cart"].queryset = Cart.objects.filter(user=user)

    cart = forms.ModelChoiceField(queryset=Cart.objects.none())

    def save(self):
        data = self.cleaned_data
        cart = data["cart"]
        cart.active = True
        cart.save()
        return cart


class CartItemNewForm(forms.Form):
    """
    This form handles the addition of a sample in the active Cart.
    The clean() method takes care of checking that the selected sample isn't
    already in the cart. It also checks that the (optionally) requested amount
    is available.
    It takes a user as parameter to retrieve the active cart.
    A valid SeedSample pk should be passed to 'seedsample' field
    """

    def __init__(self, *args, user=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.user = user

    seedsample = forms.IntegerField()
    weight = forms.FloatField(required=False)

    def clean(self):
        cleaned_data = super().clean()
        seedsample = get_object_or_404(SeedSample, pk=cleaned_data.get("seedsample"))
        weight = cleaned_data.get("weight", None)
        cart = self.user.carts.active()
        if not cart:
            e = "You did not select any cart to add to."
            raise forms.ValidationError(e)
        cartitem = CartItem.objects.filter(cart=cart, sample=seedsample)

        if cartitem.exists():
            e = f"{seedsample} is already in the selected Cart."
            raise forms.ValidationError(e)

        if weight and weight > seedsample.weight:
            e = f"There is only {seedsample.weight} grams available of {seedsample}."
            raise forms.ValidationError(e)

        return cleaned_data

    def save(self):
        cleaned_data = self.cleaned_data
        seedsample = get_object_or_404(SeedSample, pk=cleaned_data["seedsample"])
        cartitem = CartItem(cart=self.user.carts.active(), sample=seedsample)
        if weight := cleaned_data.get("weight", None):
            cartitem.weight = weight
        cartitem.save()
        return cartitem


class CartItemSetWeightForm(forms.Form):
    cartitem = forms.IntegerField(widget=forms.HiddenInput)
    weight = forms.FloatField(required=True)

    def clean(self):
        cleaned_data = super().clean()
        self.object = get_object_or_404(CartItem, pk=cleaned_data.get("cartitem"))
        weight = cleaned_data.get("weight")
        if weight and weight > self.object.sample.weight:
            e = f"There is only {self.object.sample.weight} grams available of {self.object.sample}."
            raise forms.ValidationError(e)
        return cleaned_data

    def save(self):
        self.object.weight = self.cleaned_data.get("weight")
        self.object.save()
        return self.object


class CartForm(forms.ModelForm):
    class Meta:
        model = Cart
        fields = ("name",)


class StorageCreateForm(forms.ModelForm):
    positions = forms.IntegerField(min_value=1, label="Number of available slots in this container")

    class Meta:
        model = Storage
        fields = ("name",)


class StorageUpdateForm(forms.ModelForm):
    positions = forms.IntegerField(min_value=1, label="Number of available slots in this container")

    class Meta:
        model = Storage
        fields = ("name",)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["positions"].widget.attrs["min"] = self.instance.stored_samples
        self.fields["positions"].initial = self.instance.total_positions
        self.fields["positions"].validators.append(MinValueValidator(self.instance.stored_samples))

    def save(self, *args, **kwargs):
        instance = super().save(*args, **kwargs)
        pos = self.cleaned_data["positions"]
        total_pos = instance.total_positions
        if pos > total_pos:
            instance.increase_positions(pos)
        if pos < total_pos:
            instance.decrease_positions(pos)
