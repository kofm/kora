from crispy_forms.layout import Field
from django import forms
from django_filters import FilterSet
from django_filters.filters import CharFilter

from frontpage.forms import HTMXFormMixin, generate_form_layout
from parameters.models import Parameter


class ParameterFilterForm(HTMXFormMixin, forms.Form):
    name = forms.CharField()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper.layout = generate_form_layout([Field("name")])


class ParameterFilter(FilterSet):
    name = CharFilter(lookup_expr="icontains", label="Name")

    class Meta:
        model = Parameter
        fields = ("name",)
        form = ParameterFilterForm
