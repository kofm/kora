from django import template
from django.utils.safestring import mark_safe

register = template.Library()


def _join_attrs(attrs: dict):
    return " ".join(f'{key.replace("_", "-")}="{value}"' for key, value in attrs.items())


HTMX_MODAL_ATTRS = {
    "hx_target": "#modal",
    "hx_swap": "innerHTML",
    "hx_trigger": "click",
    "data_bs_toggle": "modal",
    "data_bs_target": "#modal",
}


@register.inclusion_tag("frontpage/partials/dropdown_item.html")
def dropdown_item(label, **kwargs):
    href = kwargs.pop("href", None)
    disabled = kwargs.pop("disabled", False) == "True"
    querystring = kwargs.pop("querystring", None)
    if querystring:
        href += querystring
    attrs = _join_attrs(kwargs)
    return {"label": label, "href": href, "attrs": attrs, "disabled": disabled}


@register.inclusion_tag("frontpage/partials/dropdown_item.html")
def dropdown_item_to_modal(label, **kwargs):
    disabled = kwargs.pop("disabled", False) == "True"
    attrs = _join_attrs(kwargs)
    attrs += _join_attrs(HTMX_MODAL_ATTRS)
    return {"label": label, "attrs": attrs, "disabled": disabled}


@register.inclusion_tag("frontpage/partials/list_page_header.html")
def list_page_header(title, create_url=None):
    return {"page_title": title, "create_url": create_url}


@register.inclusion_tag("frontpage/partials/detail_page_header.html")
def detail_page_header(
    instance=None,
    title="",
    subtitle="",
    update_url=None,
    delete_url=None,
    subtitle_emphasis=False,
    **kwargs,
):
    if not title and instance:
        title = instance.__str__()
    if not update_url and instance and hasattr(instance, "get_update_url"):
        update_url = instance.get_update_url()
    if not delete_url and instance and hasattr(instance, "get_delete_url"):
        delete_url = instance.get_delete_url()
    cant_delete_msg = kwargs.get(
        "cant_delete_msg", "You can't remove this entry because it is referenced by other data."
    )
    return {
        "page_title": title,
        "subtitle": subtitle,
        "object": instance,
        "update_url": update_url,
        "delete_url": delete_url,
        "cant_delete_msg": cant_delete_msg,
        "subtitle_emphasis": subtitle_emphasis,
    }


@register.inclusion_tag("frontpage/partials/list_group_item.html")
def list_group_item(value, label, pk, update_url=None, delete_url=None, time=""):
    return {"value": value, "label": label, "pk": pk, "update_url": update_url, "delete_url": delete_url, "time": time}


@register.inclusion_tag("frontpage/partials/card_col_rows.html")
def card_col_rows(title, label, url="#"):
    return {"title": title, "label": label, "url": url}


@register.inclusion_tag("frontpage/partials/offcanvas.html", takes_context=True)
def offcanvas(context, offcanvas_id, title, template_file):
    return {
        "user": context["user"],
        "offcanvas": {
            "id": offcanvas_id,
            "title": title,
            "template_file": template_file,
        },
    }


@register.simple_tag
def modal_attrs():
    html = _join_attrs(HTMX_MODAL_ATTRS)
    return mark_safe(html)


@register.simple_tag
def offcanvas_toggle(offcanvas_id: str, content: str):
    """
    Creates a Bootstrap offcanvas toggle button.

    Usage:
    {% load components %}
    {% offcanvas_toggle "offcanvasWorkspace" "<i class='bi bi-collection'></i>" %}

    Parameters:
    - offcanvas_id: The ID of the offcanvas element (without the '#' prefix)
    - content: Optional HTML content for the toggle. Defaults to a collection icon.
    """

    cap_id = offcanvas_id.capitalize()

    # Build the HTML string
    html = f"""<a id="offcanvas{cap_id}Toggle" data-bs-toggle="offcanvas" href="#offcanvas{cap_id}"
       role="button" aria-controls="offcanvas{cap_id}">
    {content}
</a>"""

    return mark_safe(html)
