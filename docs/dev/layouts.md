# Layout Helpers

The `frontpage.layouts` module provides small layout classes to render collections of objects into reusable templates (cards, lists, grids).

All layouts:

- take an **iterable of objects** (usually a queryset),
- expose a list of “elements” to the template,
- have a `render()` method that returns the rendered HTML string.

## BaseLayout

`BaseLayout` is the core class. Other layouts build on top of it.

```python
class BaseLayout:
    template_name: str

    def __init__(self, objs: Iterable[Any]):
        self.objs = objs
```

### Responsibilities

* accepts the objects to render (`self.objs`)
* build the `elements` list for templates
* render the configured template (`template_name`)

### Assets

```python
@property
def assets(self):
    return self._assets

def add_asset(self, asset_type: str, assets: Iterable[str]) -> None:
    bucket = self._assets.setdefault(asset_type, [])
    for asset in assets:
        bucket.append(asset)
```

* `asset_type` is a string like `"css"`, `"js"`, or `"hs"` (hyperscript).
* `assets` is an iterable of strings, which are passed to `"{% static %}"`.
* The structure is: `{"css": [...], "js": [...], ...}`.

Intended use: in the view, call the helper function `frontpage.utils.assets.add_layout_assets()` to update the template `context`, so that all assets required by the layout are automatically included by the base template (see ``frontpage/base.html``). For example:

```python
def a_view(request):
	context = {}
	layout = BaseCardLayout(items)
	add_layout_assets(context, layout)
	return render(request, "my_template.html", context)
```

### Elements

```python
def get_title(self, obj):
    return str(obj)

def get_url(self, obj):
    if hasattr(obj, "get_absolute_url"):
        return obj.get_absolute_url()
    return ""

def get_item_css_class(self, obj):
    return ""
```

These methods are hooks. Subclasses usually override them:

* `get_title(obj)` – text label for the object.
* `get_url(obj)` – link target; defaults to `obj.get_absolute_url()` if present.
* `get_item_css_class(obj)` – optional CSS class per object.

```python
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
```

* `get_elements()` returns the list consumed by templates.
* `has_elements()` is a convenience helper for templates (e.g. to show empty states).

### Context and rendering

```python
def get_context_data(self) -> dict:
    return {"elements": self.get_elements()}

def render(self):
    return render_to_string(self.template_name, self.get_context_data())
```

* Templates receive a single key: `elements`.
* `render()` returns the rendered HTML string, using `self.template_name`.

## BaseListLayout

Render items in a list layout using Bootstrap's `list-group`.

```python
class BaseListLayout(BaseLayout):
    template_name = "frontpage/partials/list_layout.html"
```

## BaseCardLayout

Renders items in a simple card layout using Bootstrap's grid system (`row` and `col`).

```python
class BaseCardLayout(BaseLayout):
    template_name = "frontpage/partials/card_layout.html"
```

## BaseGridLayout

`BaseGridLayout` renders objects in a proper CSS grid, using a container template and a separate item template.

```python
class BaseGridLayout(BaseCardLayout):
    template_name = "frontpage/partials/grid.html"
    item_template_name = "frontpage/partials/grid_item.html"

    def __init__(self, *args, num_columns, item_attrs=None, container_id="grid", **kwargs):
        super().__init__(*args, **kwargs)
        self.container_id = container_id
        self.num_columns = num_columns
        self.item_attrs = item_attrs or {}
```

#### Constructor arguments

* `objs` (from `BaseLayout`): iterable of objects to render.
* `num_columns` (required): number of columns in the grid.
* `item_attrs` (optional dict): attributes to apply to each item element, e.g. `{"data-role": "card", "data-id": "..."}`.
* `container_id` (default `"grid"`): HTML id for the grid container.

#### Item attributes

```python
def get_attrs_string(self, attrs: dict) -> str:
    string = " ".join(f'{key.replace("_", "-")}="{value}"' for key, value in attrs.items())
    return mark_safe(string)
```

* Converts a dict of attributes into an HTML attribute string.
* `key`s are converted from `snake_case` to `kebab-case`.

```python
def get_body(self, obj):
    return ""

def get_item_attrs(self, obj):
    return self.get_attrs_string(self.item_attrs)
```

Hooks for subclasses:

* `get_body(obj)` – main content/body for the card (HTML string or text).
* `get_item_attrs(obj)` – per-object attributes; by default it uses `self.item_attrs`
  for every object, but you can override it to depend on `obj`.

#### Elements

```python
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
```

Each element has:

* `object`
* `title`
* `body`
* `url`
* `css_class`
* `attrs` – string of HTML attributes for the item container.

#### Context

```python
def get_context_data(self) -> dict:
    context = {
        "container_id": self.container_id,
        "num_columns": self.num_columns,
        "item_template": self.item_template_name,
        "elements": self.get_elements(),
    }
    return context
```

Context for `grid.html`:

* `container_id`: id for the outer container.
* `num_columns`: how many columns to render.
* `item_template`: path to the item template.
* `elements`: list of element dicts (see above).

`render()` is inherited and works as in `BaseLayout`.

## Usage example

Subclass `BaseGridLayout`:

```python
# myapp/layouts.py

class ArticleGridLayout(BaseGridLayout):
    def get_title(self, obj):
        return obj.title

    def get_body(self, obj):
        return obj.summary

    def get_item_css_class(self, obj):
        return "article-card"

    def get_item_attrs(self, obj):
        # Example of per-object attributes
        return self.get_attrs_string({
            "data-article-id": obj.pk,
            "data-featured": str(obj.is_featured).lower(),
        })
```

```python
# myapp/views.py

def article_list(request):
    articles = Article.objects.published().order_by("-published_at")[:12]
    layout = ArticleGridLayout(articles, num_columns=3, container_id="frontpage-articles")
    context = {"layout": layout}
    return render(request, "my_template.html", context)
```

Then in the template:

```html
{# myapp/article_list.html #}
{% extends "frontpage/base.html" %}

{# this loads the `render_layout` templatetag #}
{% load components %}

{% render_layout layout %}
```

## Summary

* `BaseLayout` builds a generic `elements` list and to be rendered in a template.
* `BaseCardLayout`, `BaseListLayout` are thin wrappers with predefined templates.
* `BaseGridLayout` adds grid-specific context (`num_columns`, `container_id`, per-item `attrs`) and supports a separate item template.
* You typically subclass these layouts and override `get_title`, `get_body`, `get_item_css_class`, and `get_item_attrs` to adapt them to your models.
