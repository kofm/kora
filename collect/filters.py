from crispy_forms.layout import Field, Layout
from django import forms
from django.db import connections
from django.db.models import Q
from django.urls import reverse_lazy
from django_filters import CharFilter, FilterSet, ModelMultipleChoiceFilter

from frontpage.forms import HTMXFormMixin, SearchAndClearButtons
from frontpage.widgets import ModelTomSelectMultiple, TomSelectConfig
from register.models import PlantSpecies


class SampleFilterForm(HTMXFormMixin, forms.Form):
    omni = forms.CharField()
    variety__species = forms.MultipleChoiceField()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper.layout = Layout(Field("omni"), Field("variety__species"), SearchAndClearButtons())
        self.helper.form_id = "sampleFilterForm"


class SampleFilter(FilterSet):
    omni = CharFilter(
        method="omni_search",
        label="Text search",
        widget=forms.TextInput(attrs={"placeholder": "Search sample ID, variety or notes..."}),
    )
    variety__species = ModelMultipleChoiceFilter(
        queryset=PlantSpecies.objects.all(),
        widget=ModelTomSelectMultiple(
            ts_config=TomSelectConfig(
                url=reverse_lazy("register:plantspecies_autocomplete"),
                value_field="id",
                label_field="common_name",
                search_field=["common_name", "botanical_name"],
                preload="true",
            )
        ),
        label="Species",
    )

    class Meta:
        form = SampleFilterForm

    def omni_search(self, queryset, _, value):
        if not value:
            return queryset
        query = Q(variety__names__name__icontains=value) | Q(notes__icontains=value)
        if value.isdecimal():
            try:
                sample_id = int(value)
            except ValueError:
                # Extremely long numeric text can exceed Python's conversion limit.
                pass
            else:
                minimum, maximum = connections[queryset.db].ops.integer_field_range("PositiveIntegerField")
                if (minimum is None or sample_id >= minimum) and (maximum is None or sample_id <= maximum):
                    query |= Q(sample_id=sample_id)
        return queryset.filter(query).distinct()
