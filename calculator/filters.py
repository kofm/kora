import django_filters
from django_filters.widgets import RangeWidget

from calculator.models import Crop
from register.models import PlantSpecies
from spaces.models import Area


class CropFilter(django_filters.FilterSet):
    area = django_filters.ModelMultipleChoiceFilter(queryset=Area.objects.all())
    species = django_filters.ModelMultipleChoiceFilter(queryset=PlantSpecies.objects.all())
    sowing = django_filters.DateFromToRangeFilter(
        label="Sowing range",
        widget=RangeWidget(attrs={"type": "date"}),
        method="filter_my_date",
    )

    class Meta:
        model = Crop
        fields = ["species", "area"]

    def filter_my_date(self, queryset, _, value):
        queryset = queryset.filter(management__type__code="sowing")

        if not value.stop:
            return queryset.filter(
                management__date__gte=value.start,
            )
        if not value.start:
            return queryset.filter(
                management__date__lte=value.stop,
            )

        return queryset.filter(
            management__date__range=[value.start, value.stop],
        )
