from django import template

register = template.Library()


@register.inclusion_tag("django_sortable_htmx/sortable_grid.html")
def render_sortable_grid(
    queryset,
    element_id,
    element_class,
    sort_url,
    cols: int,
    *,
    item_template: str = "django_sortable_htmx/grid_item.html",
    is_sortable: bool = True,
):
    return {
        "object_list": queryset,
        "element_id": element_id,
        "element_class": element_class,
        "sort_url": sort_url,
        "item_template": item_template,
        "cols": cols,
        "is_sortable": is_sortable,
    }
