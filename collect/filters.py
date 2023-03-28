import django_filters
from django.db.models import Q
from .models import SeedSample


class SeedSampleFilter(django_filters.FilterSet):
    growing_season__lt = django_filters.NumberFilter(field_name='growing_season', lookup_expr='lt')
    query = django_filters.CharFilter(method="universal_search", label="Variety")

    class Meta:
        model = SeedSample
        fields = ["query", "growing_season__lt"]

    def universal_search(self, queryset, name, value):
        return SeedSample.objects.filter(
            Q(variety__names__name__icontains=value) | Q(notes__icontains=value)
        )
