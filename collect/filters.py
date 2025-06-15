from crispy_forms.layout import Field, Layout
from django import forms
from django.db.models import Q
from django_filters import CharFilter, FilterSet, ModelMultipleChoiceFilter

from collect.models import Sample
from frontpage.forms import HTMXFormMixin, SearchAndClearButtons
from frontpage.widgets import TomSelectMultiple
from register.models import PlantSpecies


class SampleFilterForm(HTMXFormMixin, forms.Form):
    omni = forms.CharField()
    variety__species = forms.MultipleChoiceField()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper.layout = Layout(Field("omni"), Field("variety__species"), SearchAndClearButtons())


class SampleFilter(FilterSet):
    omni = CharFilter(
        method="omni_search",
        label="Text search",
        widget=forms.TextInput(attrs={"placeholder": "Search variety or notes..."}),
    )
    variety__species = ModelMultipleChoiceFilter(
        queryset=PlantSpecies.objects.all(),
        widget=TomSelectMultiple(),
        label="Species",
    )

    class Meta:
        form = SampleFilterForm

    def omni_search(self, queryset, name, value):
        return Sample.objects.filter(Q(variety__names__name__icontains=value) | Q(notes__icontains=value))
