from django.core.exceptions import ImproperlyConfigured
from django.db.models import Model, Q, QuerySet
from django.http import JsonResponse
from django.views import View


class AutocompleteModelView(View):
    model: type[Model] | None = None
    search_fields = ["name"]
    value_fields = ["id", "name"]
    ordering = []
    page_size = 100
    filter_by = []

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

    def get(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        queryset = self.filter_queryset(queryset)
        if self.ordering:
            queryset = queryset.order_by(*self.ordering)
        queryset = queryset.values(*self.value_fields)
        queryset = queryset[: self.page_size]

        return JsonResponse({"results": list(queryset)})
