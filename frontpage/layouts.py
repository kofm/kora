from collections.abc import Iterable
from typing import Any

from django.template.loader import render_to_string
from django.utils.safestring import mark_safe


class BaseLayout:
    template_name: str
    item_template_name: str

    def __init__(self, objs: Iterable[Any]):
        self.objs = objs
        self._assets: dict[str, list[str]] = {}

    @property
    def assets(self) -> dict[str, list[str]]:
        return self._assets

    def add_asset(self, asset_type: str, assets: Iterable[str]) -> None:
        bucket = self._assets.setdefault(asset_type, [])
        for asset in assets:
            bucket.append(asset)

    def get_title(self, obj):
        return str(obj)

    def get_url(self, obj):
        if hasattr(obj, "get_absolute_url"):
            return obj.get_absolute_url()
        return ""

    def get_item_css_class(self, obj):
        return ""

    def get_elements(self) -> list:
        elements = []
        for obj in self.objs:
            element = {
                "object": obj,
                "title": self.get_title(obj),
                "url": self.get_url(obj),
                "css_class": self.get_item_css_class(obj),
            }
            elements.append(element)
        return elements

    def has_elements(self):
        return bool(self.objs)

    def get_context_data(self) -> dict:
        return {
            "item_template_name": self.item_template_name,
            "elements": self.get_elements(),
        }

    def render(self):
        return render_to_string(self.template_name, self.get_context_data())


class BaseCardLayout(BaseLayout):
    template_name = "frontpage/partials/card_layout.html"
    item_template_name = "frontpage/partials/card_item.html"


class BaseListLayout(BaseLayout):
    template_name = "frontpage/partials/list_layout.html"


class BaseGridLayout(BaseLayout):
    template_name = "frontpage/partials/grid.html"
    item_template_name = "frontpage/partials/grid_item.html"

    def __init__(
        self,
        *args,
        num_columns,
        item_attrs=None,
        container_id="grid",
        selectable=False,
        show_coordinates=False,
        **kwargs,
    ) -> None:
        super().__init__(*args, **kwargs)
        self.container_id = container_id
        self.num_columns = num_columns
        self.item_attrs = item_attrs or {}
        self.selectable = selectable
        self.show_coordinates = show_coordinates

    def get_attrs_string(self, attrs: dict) -> str:
        string = " ".join(f'{key.replace("_", "-")}="{value}"' for key, value in attrs.items())
        return mark_safe(string)

    def get_body(self, obj):
        return ""

    def get_item_attrs(self, obj):
        return self.get_attrs_string(self.item_attrs)

    def get_elements(self) -> list:
        elements = []
        for obj in self.objs:
            element = {
                "object": obj,
                "title": self.get_title(obj),
                "body": self.get_body(obj),
                "url": self.get_url(obj),
                "css_class": self.get_item_css_class(obj),
                "attrs": self.get_item_attrs(obj),
            }
            elements.append(element)
        return elements

    def get_context_data(self, **kwargs) -> dict:
        context = super().get_context_data(**kwargs)
        element_count = len(context["elements"])
        row_count = (element_count + self.num_columns - 1) // self.num_columns
        context.update(
            {
                "container_id": self.container_id,
                "num_columns": self.num_columns,
                "selectable": self.selectable,
                "show_coordinates": self.show_coordinates and element_count > 0,
                "column_indices": range(1, self.num_columns + 1),
                "row_indices": range(row_count, 0, -1),
            }
        )
        return context

    def render(self):
        return render_to_string(self.template_name, self.get_context_data())
