from django.db.models import Q, QuerySet


def _filter_descriptions(queryset: QuerySet, states: list) -> QuerySet:
    return queryset.filter(Q(expressions__state__in=states) | Q(expressions__state__related_states__in=states))
