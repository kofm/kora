import django_filters
from describe.models import Description


class NumberInFilter(django_filters.BaseInFilter, django_filters.NumberFilter):
    pass


class DescriptionFilter(django_filters.FilterSet):
    description = NumberInFilter(field_name="description", lookup_expr="in", label="Description IDs")
    variety = NumberInFilter(field_name="variety__pk", lookup_expr="in", label="Variety IDs")

    class Meta:
        model = Description
        fields = {"name": ["exact", "icontains"]}
