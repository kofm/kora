from django import forms
from django.db.models import Q
from django.forms.widgets import HiddenInput
from django.utils.translation import gettext_lazy as _
from crispy_forms.helper import FormHelper
from crispy_forms.layout import HTML, Layout, Field

from collect.models import Germinability, SampleWeight, SeedSample, StoragePosition


class TomSelectWidget(forms.Select):
    class Media:
        css = {
            "all": ("https://cdn.jsdelivr.net/npm/tom-select/dist/css/tom-select.css",)
        }
        js = (
            "https://cdn.jsdelivr.net/npm/tom-select/dist/js/tom-select.complete.min.js",
        )


class SeedSampleForm(forms.ModelForm):
    tomvar = forms.CharField(label="Variety")
    tompos = forms.CharField(label="Position")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # self.fields['position'].queryset = StoragePosition.objects.filter(Q(seedsample__id=self.instance.pk) | Q(seedsample__isnull=True))
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


class GerminabilityForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        # first call parent's constructor
        super(GerminabilityForm, self).__init__(*args, **kwargs)
        # there's a `fields` property now
        self.fields["germinability"].required = False

    class Meta:
        model = Germinability
        fields = ("germinability", "after_days", "performed_at")


class SeedSampleYearForm(forms.Form):
    year = forms.ChoiceField(
        choices=[
            (0, ""),
        ]
        + list(
            SeedSample.objects.filter(growing_season__isnull=False)
            .order_by("growing_season")
            .distinct("growing_season")
            .values_list("growing_season", "growing_season")
        ),
        widget=forms.Select(
            attrs={
                "class": "form-select",
                "hx-get": "_hx",
                "hx-trigger": "change",
                "hx-target": "#seedsample-table",
                "hx-include": "#search-form"
                # 'onchange': 'this.parentElement.submit()'
            }
        ),
    )
