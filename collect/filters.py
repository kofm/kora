import django_filters
from django.db.models import Q

from .models import Sample


class SampleFilter(django_filters.FilterSet):
    query = django_filters.CharFilter(method="universal_search", label="")

    class Meta:
        model = Sample
        fields = ("query",)

    def universal_search(self, queryset, name, value):
        return Sample.objects.filter(Q(variety__names__name__icontains=value) | Q(notes__icontains=value))
