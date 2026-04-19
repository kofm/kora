from typing import Any, Protocol, cast

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


class BaseSortableGridLayout(SortableLayoutMixin, BaseGridLayout):
    template_name = "django_sortable_htmx/grid.html"
    item_template_name = "django_sortable_htmx/grid_item.html"
