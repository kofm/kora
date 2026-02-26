from crispy_forms.bootstrap import FieldWithButtons, StrictButton
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Field, Layout
from django import forms
from django.core.validators import MinValueValidator
from django.forms.widgets import DateInput
from django.urls import reverse

from collect.models import (
    Cart,
    CartItem,
    Germinability,
    Sample,
    SampleWeight,
    Storage,
    StoragePosition,
)
from frontpage.widgets import TomSelect, YearInput


class SampleForm(forms.ModelForm):
    class Meta:
        model = Sample
        fields = ("sample_id", "variety", "position", "growing_season", "notes")
        widgets = {
            "variety": TomSelect,
            "position": TomSelect,
            "growing_season": YearInput,
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        sample_id = Sample.objects.next_id()
        self.fields["sample_id"].initial = sample_id
        empty_positions = StoragePosition.objects.empty_positions_for_sample(self.instance.pk)
        self.fields["position"].queryset = empty_positions
        self.fields["position"].initial = empty_positions.first()


class SampleWeightForm(forms.ModelForm):
    class Meta:
        model = SampleWeight
        fields = ("weight", "created_at")
        widgets = {
            "created_at": DateInput(attrs={"type": "date"}),
        }


class SampleRestoreForm(forms.ModelForm):
    class Meta:
        model = Sample
        fields = ("position",)
        widgets = {"position": TomSelect}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        empty_positions = StoragePosition.objects.empty_positions_for_sample(self.instance.pk)
        self.fields["position"].queryset = empty_positions
        self.fields["position"].initial = empty_positions.first()


class GerminabilityForm(forms.ModelForm):
    class Meta:
        model = Germinability
        fields = ("germinability", "after_days", "performed_at")
        widgets = {
            "performed_at": DateInput(attrs={"type": "date"}),
        }


class CartSelectForm(forms.Form):
    cart = forms.ModelChoiceField(queryset=Cart.objects.none(), label="Active Cart", required=False)

    def __init__(self, *args, user=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.user = user
        carts = Cart.objects.filter(user=self.user)
        self.fields["cart"].queryset = carts
        self.helper = FormHelper(self)
        self.helper.layout = Layout(
            Field(
                "cart",
                css_class="form-select",
                hx_post=reverse("collect:cart_activate"),
                hx_trigger="change",
                hx_target="#cartBody",
            ),
        )

    def save(self):
        cart = self.cleaned_data.get("cart")
        Cart.objects.filter(user=self.user).deactivate_all()
        if cart:
            cart.is_active = True
            cart.save()
        return cart


class CartItemUpdateForm(forms.ModelForm):
    class Meta:
        model = CartItem
        fields = ("weight",)


class CartCreateForm(forms.ModelForm):
    class Meta:
        model = Cart
        fields = ("name", "kind")


class CartUpdateForm(forms.ModelForm):
    class Meta:
        model = Cart
        fields = ("name",)


class CartDefaultWeightForm(forms.ModelForm):
    class Meta:
        model = Cart
        fields = ("default_weight",)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.attrs = {
            "hx_post": reverse("collect:cart_set_default_weight", args=(self.instance.pk,)),
            "hx_swap": "none",
        }
        self.helper.layout = Layout(
            FieldWithButtons(
                Field("default_weight"),
                StrictButton(
                    "<i class='bi bi-check'></i>",
                    css_class="btn btn-outline-success",
                    type="submit",
                ),
            )
        )


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
        self.fields["positions"].widget.attrs["min"] = self.instance.stored_positions
        self.fields["positions"].initial = self.instance.total_positions
        self.fields["positions"].validators.append(MinValueValidator(self.instance.stored_positions))

    def save(self, *args, **kwargs):
        instance = super().save(*args, **kwargs)
        pos = self.cleaned_data["positions"]
        total_pos = instance.total_positions
        if pos > total_pos:
            instance.increase_positions(pos)
        if pos < total_pos:
            instance.decrease_positions(pos)
