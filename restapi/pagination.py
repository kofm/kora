from rest_framework.pagination import PageNumberPagination


class OptionalPagination(PageNumberPagination):
    def paginate_queryset(self, queryset, request, view=None):
        if request.query_params.get("no_pagination") == "1":
            return None
        return super().paginate_queryset(queryset, request, view)
