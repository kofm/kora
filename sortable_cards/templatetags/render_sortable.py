from django import template

register = template.Library()


@register.inclusion_tag("sortable_cards/sortable_card_div.html")
def render_sortable(
    queryset,
    element_id,
    element_class,
    sort_url,
    item_template="sortable_cards/card.html",
    is_sortable=True,
    extra_item=None
):
    """
    Renders sortable items.

    :param queryset: The queryset of objects to render.
    :param element_id: The ID for the sortable container.
    :param element_class: The class for the sortable container.
    :param sort_url: URL for htmx sorting endpoint (see SortableView class).
    :param item_template: Template for each item (default: "sortable_cards/card.html").
    :param is_sortable: Boolean indicating if the items are sortable (default: True).
    :param extra_item
    :return: Rendered HTML for the sortable container.
    """

    return {
        "sortable": {
            "object_list": queryset,
            "element_id": element_id,
            "element_class": element_class,
            "sort_url": sort_url,
            "item_template": item_template,
            "is_sortable": is_sortable,
            "extra_item": extra_item,
        }
    }
