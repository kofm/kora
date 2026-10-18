"""Common typed value filters, including ranges across both numeric types."""

from math import ceil, floor

from django import forms
from django.db.models import Q
from django_filters import BooleanFilter, CharFilter, DateFilter, FilterSet, NumberFilter


class TypedValueFilter(FilterSet):
    value = NumberFilter(method="filter_number")
    value_min = NumberFilter(method="filter_number_min", label="Value minimum")
    value_max = NumberFilter(method="filter_number_max", label="Value maximum")
    value_boolean = BooleanFilter()
    value_text = CharFilter(lookup_expr="icontains", label="Text contains")
    value_date_start = DateFilter(
        field_name="value_date",
        lookup_expr="gte",
        label="Value date from",
        widget=forms.DateInput(attrs={"type": "date"}),
    )
    value_date_end = DateFilter(
        field_name="value_date",
        lookup_expr="lte",
        label="Value date through",
        widget=forms.DateInput(attrs={"type": "date"}),
    )

    def filter_number(self, queryset, name, value):
        condition = Q(value_decimal=value)
        if value == int(value):
            condition |= Q(value_integer=int(value))
        return queryset.filter(condition)

    def filter_number_min(self, queryset, name, value):
        return queryset.filter(Q(value_decimal__gte=value) | Q(value_integer__gte=ceil(value)))

    def filter_number_max(self, queryset, name, value):
        return queryset.filter(Q(value_decimal__lte=value) | Q(value_integer__lte=floor(value)))
