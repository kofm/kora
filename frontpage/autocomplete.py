"""Class-based view to provide server-side autocomplete for TomSelect widgets."""

from django.core.exceptions import ImproperlyConfigured
from django.db.models import Model, Q, QuerySet
from django.http import JsonResponse
from django.views import View


class AutocompleteModelView(View):
    """Provide autocomplete data to TomSelect remote widgets.

    :param model: the target Model
    :param search_fields: the lookup fields
    :param value_fiels: the fields to return in the results data
    :param ordering: the ordering to applyt to the results
    :param page_size: the number of results per page
    :param filter_by: the fields to filter the results by, for dependant widgets

    Each results row always include a `text` key (which is the default
    TomSelect's `labelField`), which contains the string
    representation of the object.

    `hook_queryset` methods can be used e.g. to select/prefetch
    related models.

    """

    model: type[Model] | None = None
    search_fields: list = ["name"]
    value_fields: list = ["id", "name"]
    ordering: list = []
    page_size: int = 100
    filter_by: list = []

    def hook_queryset(self, queryset: QuerySet) -> QuerySet:
        return queryset

    def get_queryset(self) -> QuerySet:
        if self.model is None:
            raise ImproperlyConfigured(f"{self.__class__.__name__} requires a `model` attribute to be set.")
        queryset = self.model.objects.all()
        queryset = self.hook_queryset(queryset)

        return queryset

    def get_search_query(self):
        return self.request.GET.get("q", "").strip()

    def filter_by_queryset(self, queryset):
        cond = Q()
        for flt in self.filter_by:
            val = self.request.GET.get(flt)
            cond &= Q(**{flt: val})
        return queryset.filter(cond)

    def filter_queryset(self, queryset):
        queryset = self.filter_by_queryset(queryset)

        query = self.get_search_query()
        if not query:
            return queryset

        condition = Q()
        for field in self.search_fields:
            condition |= Q(**{f"{field}__icontains": query})

        return queryset.filter(condition)

    def get_label(self, obj):
        return str(obj)

    def get_row(self, obj):
        return {
            **{field: getattr(obj, field) for field in self.value_fields},
            "text": self.get_label(obj),
        }

    def get_results(self, queryset):
        return [self.get_row(obj) for obj in queryset]

    def get(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        queryset = self.filter_queryset(queryset)
        if self.ordering:
            queryset = queryset.order_by(*self.ordering)
        queryset = queryset[: self.page_size]
        results = self.get_results(queryset)

        return JsonResponse({"results": results})
