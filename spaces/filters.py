from crispy_forms.layout import Field, Layout
from django import forms
from django_filters import (
    CharFilter,
    FilterSet,
)

from frontpage.forms import HTMXFormMixin, SearchAndClearButtons
from spaces.models import Location


class LocationFilterForm(HTMXFormMixin, forms.Form):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper.layout = Layout(Field("name"), SearchAndClearButtons())


class LocationFilter(FilterSet):
    name = CharFilter(label="Search", lookup_expr="icontains")

    class Meta:
        fields = ("name",)
        model = Location
        form = LocationFilterForm
