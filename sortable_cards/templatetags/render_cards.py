from django import template

register = template.Library()


@register.inclusion_tag("sortable_cards/sortable_div.html")
def render_cards(queryset, element_id, sort_url, card_template="sortable_cards/card.html", new_url=None, is_sortable=True):
    return {
        "object_list": queryset,
        "element_id": element_id,
        "sort_url": sort_url,
        "card_template": card_template,
        "is_sortable": is_sortable,
        "new_url": new_url,
    }
