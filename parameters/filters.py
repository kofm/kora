from crispy_forms import layout
from django import forms
from django.db.models import Q
from django_filters import FilterSet
from django_filters.filters import CharFilter

from frontpage.forms import HTMXFormMixin
from parameters.models import Parameter


class ParameterFilterForm(HTMXFormMixin, forms.Form):
    name = forms.CharField()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper.layout = layout.Layout(
            layout.Field("search"),
            layout.Div(
                layout.Submit("search", "Search", css_class="btn-sm"),
                layout.HTML('<a class="btn btn-sm btn-secondary" href=".">Clear</a>'),
                css_class="mt-0 mb-3",
            ),
        )


class ParameterFilter(FilterSet):
    search = CharFilter(label="Parameter", method="filter_name")

    class Meta:
        model = Parameter
        fields = ("search",)
        form = ParameterFilterForm

    def filter_name(self, queryset, name, value):
        query = Q(code__icontains=value)
        query |= Q(name__icontains=value)
        query |= Q(description__icontains=value)
        return queryset.filter(query)
