import django_filters
from django.db.models import Q
from .models import SeedSample


class SeedSampleFilter(django_filters.FilterSet):
    query = django_filters.CharFilter(method="universal_search", label="")

    class Meta:
        model = SeedSample
        fields = ["query"]

    def universal_search(self, queryset, name, value):
        return SeedSample.objects.filter(
            Q(variety__names__name__icontains=value) | Q(notes__icontains=value)
        )
