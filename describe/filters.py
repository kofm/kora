import django_filters
from django.forms import TextInput

from describe.models import Description


class DescriptionFilterByName(django_filters.FilterSet):
    variety__names__name = django_filters.CharFilter(
        label="Variety name",
        lookup_expr="unaccent__lower__trigram_similar",
        widget=TextInput(attrs={"placeholder": "Type to search..."}),
    )

    class Meta:
        model = Description
        fields = ["variety__names__name"]
