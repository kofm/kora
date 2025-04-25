from crispy_forms.bootstrap import FieldWithButtons, StrictButton
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Field, Layout
from django import forms
from django.core.validators import MinValueValidator
from django.forms.widgets import DateInput, HiddenInput
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


class SampleForm2(forms.ModelForm):
    class Meta:
        model = Sample
        fields = ("sample_id", "variety", "position", "growing_season")
        widgets = {
            "variety": TomSelect,
            "position": TomSelect,
            "growing_season": YearInput,
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        sample_id = Sample.objects.next_id()
        self.fields["sample_id"].initial = sample_id
        empty_positions = StoragePosition.objects.empty_positions_for_accession(self.instance.pk)
        self.fields["position"].queryset = empty_positions
        self.fields["position"].initial = empty_positions.first()


class SampleForm(forms.ModelForm):
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
        model = Sample
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
        fields = ("weight", "created_at")
        widgets = {
            "created_at": DateInput(attrs={"type": "date"}),
        }


class GerminabilityForm(forms.ModelForm):
    class Meta:
        model = Germinability
        fields = ("germinability", "after_days", "performed_at")
        widgets = {
            "performed_at": DateInput(attrs={"type": "date"}),
        }


class SampleYearForm(forms.Form):
    year = forms.ChoiceField(
        choices=((0, ""),),
        widget=forms.Select(
            attrs={
                "class": "form-select",
                "hx-get": "_hx",
                "hx-trigger": "change",
                "hx-target": "#sample-table",
                "hx-include": "#search-form",
            }
        ),
    )


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


class CartItemSetWeightForm(forms.Form):
    cartitem = forms.IntegerField(widget=forms.HiddenInput)
    weight = forms.FloatField(required=False)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        cartitem_id = self.initial["cartitem"]
        url = reverse("collect:cartitem_set_weight", args=(cartitem_id,))
        target_id = f"#weight_{cartitem_id}"
        self.helper = FormHelper(self)
        self.helper.action = url
        form_attrs = {
            "hx_post": url,
            "hx_trigger": "change, blur, keyup[key=='Enter']",
            "hx_target": target_id,
            "hx_swap": "outerHTML",
            "hx_include": "#id_cartitem",
        }
        self.helper.attrs = form_attrs
        self.helper.layout = Layout(
            Field("cartitem"),
            FieldWithButtons(
                Field("weight", css_class="form-control"),
                StrictButton(
                    "<i class='bi bi-x'></i>",
                    css_class="btn btn-outline-secondary",
                    hx_get=url,
                    hx_trigger="click",
                    hx_vals='{"cancel": "true"}',
                ),
                StrictButton(
                    "<i class='bi bi-check'></i>",
                    css_class="btn btn-outline-success",
                ),
            ),
        )

    # FieldWithButtons(
    #                 Field("name", script=script),
    #                 StrictButton(
    #                     "<i class='bi bi-check'></i>",
    #                     css_class="btn btn-outline-success",
    #                     type="submit",
    #                 ),
    #             )

    def clean(self):
        cleaned_data = super().clean()
        cartitem_id = cleaned_data.get("cartitem")
        weight = cleaned_data.get("weight")

        self.object = CartItem.objects.select_related("sample").get(pk=cartitem_id)
        if weight and weight > self.object.sample.weight:
            e = f"There is only {self.object.sample.weight} grams available of {self.object.sample}."
            raise forms.ValidationError(e)
        return cleaned_data

    def save(self):
        weight = self.cleaned_data.get("weight", None)
        if weight:
            self.object.weight = weight
            self.object.save()
        return self.object


class CartInputForm(forms.ModelForm):
    class Meta:
        model = Cart
        fields = ("name",)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["name"].label_suffix = ""
        self.fields["name"].help_text = ""
        self.helper = FormHelper(self)
        script = f"""
        on click from elsewhere wait 100ms then fetch
        {reverse("collect:cart_detail")} then put the result into
        #cartBody then call htmx.process(#cartBody)
        """
        self.helper.layout = Layout(
            FieldWithButtons(
                Field("name", script=script),
                StrictButton(
                    "<i class='bi bi-check'></i>",
                    css_class="btn btn-outline-success",
                    type="submit",
                ),
            )
        )


class CartCreateForm(CartInputForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["name"].label = "Create Cart"
        self.helper.attrs = {"hx_post": reverse("collect:cart_create")}


class CartUpdateForm(CartInputForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["name"].label = "Rename Cart"
        self.helper.attrs = {"hx_post": reverse("collect:cart_update", args=(self.instance.pk,))}


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
