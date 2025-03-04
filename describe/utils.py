from typing import Sequence
from django.db.models import Q, QuerySet


def get_first_item_by_key(list, value, key):
    return next(filter(lambda x: x[key] == value, list))


def merge_unique(base: QuerySet, addition, key) -> Sequence | None:
    addition_keys = [x[key] for x in addition]
    return [
        get_first_item_by_key(addition, list_item[key], key) if list_item[key] in addition_keys else list_item
        for list_item in base
    ]


def _filter_descriptions(queryset: QuerySet, states: list) -> QuerySet:
    return queryset.filter(Q(expressions__state__in=states) | Q(expressions__state__related_states__in=states))


def delete_get_param(request, parameter):
    copy = request.GET.copy()
    del copy[parameter]
    return copy


def descriptionsuserlist_get_active(request):
    if request.user.is_authenticated:
        desclist = request.user.workspace_set.filter(is_active=True)
        if desclist.exists():
            return desclist.first()
    return None
