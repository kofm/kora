from itertools import groupby
from operator import attrgetter
from typing import Any, Protocol, cast

from django.template.defaulttags import GroupedResult
from django.urls import reverse

from frontpage.layouts import BaseGridLayout, BaseLayout


class HasContextData(Protocol):
    def get_context_data(self) -> dict[str, Any]: ...


class SortableLayoutMixin:
    """
    Mixin that assumes some base class in the MRO provides get_context_data().
    """

    def __init__(self, *args, sort_view: str, is_sortable: bool = True, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.sort_url = reverse(sort_view)
        self.is_sortable = is_sortable

    def get_context_data(self) -> dict[str, Any]:
        parent = cast(HasContextData, super())
        context = parent.get_context_data()
        context.update(
            {
                "sort_url": self.sort_url,
                "is_sortable": self.is_sortable,
            }
        )
        return context

    def switch_sortable(self, yesno: bool) -> None:
        self.is_sortable = yesno


class BaseSortableCardLayout(SortableLayoutMixin, BaseLayout):
    template_name = "django_sortable_htmx/card_layout.html"
    item_template_name = "django_sortable_htmx/card_item.html"


class BaseSortableGridLayout(SortableLayoutMixin, BaseGridLayout):
    template_name = "django_sortable_htmx/grid.html"
    item_template_name = "django_sortable_htmx/grid_item.html"


class GroupedSortableCardLayout(BaseSortableCardLayout):
    template_name = "django_sortable_htmx/grouped_card_layout.html"
    inner_template_name = "django_sortable_htmx/card_layout.html"
    item_template_name = "django_sortable_htmx/card_item.html"

    def __init__(self, *args, group_by: str, **kwargs):
        super().__init__(*args, **kwargs)
        self.group_by = group_by

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({"inner_template_name": self.inner_template_name})
        return context

    def get_elements(self):
        elements = []
        for obj in self.objs:
            element = {
                "object": obj,
                "title": self.get_title(obj),
                "url": self.get_url(obj),
                "css_class": self.get_item_css_class(obj),
                "group": attrgetter(self.group_by)(obj),
            }
            elements.append(element)
        return [GroupedResult(grouper=key, list=list(val)) for key, val in groupby(elements, lambda obj: obj["group"])]
