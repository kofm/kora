from crispy_forms.bootstrap import FieldWithButtons, StrictButton
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Field, Layout
from django import forms
from django.core.validators import MinValueValidator
from django.forms import ModelChoiceField
from django.urls import reverse, reverse_lazy

from collect.models import (
    Cart,
    CartItem,
    Germinability,
    Sample,
    SampleWeight,
    Storage,
    StoragePosition,
)
from describe.forms import TomSelectModelChoiceField
from frontpage.forms import TomSelectModelFormMixin
from frontpage.widgets import ModelTomSelect, TomSelect, TomSelectConfig, YearInput
from register.models import PlantSpecies, PlantVariety


class SampleForm(TomSelectModelFormMixin, forms.ModelForm):
    species = TomSelectModelChoiceField(
        queryset=PlantSpecies.objects.all(),
        widget=ModelTomSelect(
            ts_config=TomSelectConfig(
                url=reverse_lazy("register:plantspecies_autocomplete"),
                value_field="id",
                label_field="common_name",
                search_field=["common_name", "latin_name"],
            )
        ),
    )
    variety = TomSelectModelChoiceField(
        queryset=PlantVariety.objects.none(),
        widget=ModelTomSelect(
            ts_config=TomSelectConfig(
                url=reverse_lazy("register:variety_autocomplete"),
                value_field="id",
                label_field="name",
                search_field="name",
                depends_on="species",
                depends_param="species_id",
            ),
        ),
    )

    position = ModelChoiceField(
        queryset=StoragePosition.objects.all(),
        widget=ModelTomSelect(
            ts_config=TomSelectConfig(
                url=reverse_lazy("collect:storage_autocomplete"),
                value_field="id",
            ),
        ),
    )

    class Meta:
        model = Sample
        fields = ("sample_id", "species", "variety", "position", "growing_season", "notes")
        widgets = {
            "growing_season": YearInput,
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        sample_id = Sample.objects.next_id()
        self.fields["sample_id"].initial = sample_id


class SampleWeightForm(forms.ModelForm):
    class Meta:
        model = SampleWeight
        fields = ("weight", "created_at")
        widgets = {"created_at": forms.DateTimeInput(attrs={"type": "datetime-local"})}


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
        widgets = {"performed_at": forms.DateTimeInput(attrs={"type": "datetime-local"})}


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
        min_positions = max(1, self.instance.highest_stored_position)
        self.fields["positions"].widget.attrs["min"] = min_positions
        self.fields["positions"].initial = self.instance.total_positions
        self.fields["positions"].validators.append(MinValueValidator(min_positions))

    def save(self, commit=True):
        instance = super().save(commit=False)

        # We don't save the Storage instance if the name has not been
        # changed
        if commit:
            if "name" in self.changed_data:
                instance.save(update_fields=["name"])

            instance.set_positions(self.cleaned_data["positions"])
            self.save_m2m()

        return instance
