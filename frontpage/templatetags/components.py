from dataclasses import dataclass
from typing import Protocol, runtime_checkable

from django import template
from django.contrib.auth import get_permission_codename
from django.template.exceptions import TemplateSyntaxError
from django.urls import NoReverseMatch, reverse
from django.utils.html import format_html
from django.utils.safestring import mark_safe

from frontpage.layouts import BaseLayout
from frontpage.navigation import BasePrevNextNav
from frontpage.utils.models import model_from_label
from frontpage.utils.permissions import get_permission_from_instance
from persefone import settings

register = template.Library()


@runtime_checkable
class HasCreateUrl(Protocol):
    @classmethod
    def get_create_url(cls) -> str: ...


def _join_attrs(attrs: dict):
    return " ".join(f'{key.replace("_", "-")}="{value}"' for key, value in attrs.items())


HTMX_MODAL_ATTRS = {
    "hx_target": "#modal",
    "hx_swap": "innerHTML",
    "hx_trigger": "click",
    "data_bs_toggle": "modal",
    "data_bs_target": "#modal",
}


@register.simple_tag
def is_public():
    return settings.PUBLIC


@register.inclusion_tag("frontpage/partials/dropdown_item.html")
def dropdown_item(label, **kwargs):
    href = kwargs.pop("href", "#")
    disabled = kwargs.pop("disabled", False) == "True"
    querystring = kwargs.pop("querystring", None)
    if querystring:
        href += querystring
    attrs = _join_attrs(kwargs)
    return {
        "label": label,
        "href": href,
        "attrs": attrs,
        "disabled": disabled,
    }


@register.inclusion_tag("frontpage/partials/dropdown_item.html")
def dropdown_item_to_modal(label, **kwargs):
    disabled = kwargs.pop("disabled", False) == "True"
    attrs = _join_attrs(kwargs)
    attrs += _join_attrs(HTMX_MODAL_ATTRS)
    return {"label": label, "attrs": attrs, "disabled": disabled}


@dataclass(slots=True)
class ListPageHeader:
    page_title: str
    subtitle: str | None = None
    create_url: str | None = None
    modal: bool = False

    @classmethod
    def from_model_label(
        cls,
        request,
        model_label: str,
        *,
        title: str = "",
        subtitle: str = "",
        modal: bool = False,
    ) -> "ListPageHeader":
        user = request.user

        try:
            model = model_from_label(model_label)
        except (ValueError, LookupError) as exc:
            raise TemplateSyntaxError(str(exc)) from exc

        meta = model._meta

        verbose_plural = meta.verbose_name_plural or ""
        page_title = title or verbose_plural.title()

        permission_codename = get_permission_codename("add", meta)
        add_permission = f"{meta.app_label}.{permission_codename}"

        create_url: str | None = None
        if user.has_perm(add_permission) and isinstance(model, HasCreateUrl):
            create_url = model.get_create_url()

        return cls(
            page_title=page_title,
            subtitle=subtitle,
            create_url=create_url,
            modal=modal,
        )


@register.inclusion_tag("frontpage/partials/list_page_header.html", takes_context=True)
def list_page_header(context, model_label: str, title: str = "", subtitle: str = "", modal: bool = False):
    """
    model_label: 'app_label.ModelName' or model._meta.label_lower
    Example: 'plants.PlantVariety' or 'plants.plantvariety'
    """
    header = ListPageHeader.from_model_label(
        context["request"],
        model_label,
        title=title,
        subtitle=subtitle,
        modal=modal,
    )
    return {"header": header}


@register.inclusion_tag("frontpage/partials/detail_section_header.html", takes_context=True)
def detail_section_header(context, title, create_url=None, permission=None, create_modal=False, **kwargs):
    user = context["request"].user
    if user.has_perm(permission):
        try:
            create_url = reverse(create_url) if create_url else None
        except NoReverseMatch:
            pass
    else:
        create_url = None
    title_class = kwargs.pop("title_class", "")
    return {
        "page_title": title,
        "create_url": create_url,
        "title_class": title_class,
        "create_modal": create_modal,
    }


@register.simple_tag()
def hx_vals_use_block(block):
    return format_html('hx-vals=\'{{"use_block": "{}"}}\'', block)


def get_action_url_from_instance(action, instance):
    method = f"get_{action}_url"
    if instance and hasattr(instance, method):
        return getattr(instance, method)
    return None


@register.inclusion_tag("frontpage/partials/detail_page_header.html", takes_context=True)
def detail_page_header(context, instance, title="", subtitle="", subtitle_emphasis=False):
    user = context["request"].user
    title = title or str(instance)
    update_permission = get_permission_from_instance("change", instance)
    delete_permission = get_permission_from_instance("delete", instance)

    if user.has_perm(update_permission):
        update_url = get_action_url_from_instance("update", instance)
    else:
        update_url = None

    if user.has_perm(delete_permission):
        delete_url = get_action_url_from_instance("delete", instance)
    else:
        delete_url = None

    if hasattr(instance, "cant_delete_msg"):
        cant_delete_msg = instance.cant_delete_msg
    else:
        cant_delete_msg = "You can't remove this entry because it is associated to other data."

    return {
        "title": title,
        "subtitle": subtitle,
        "object": instance,
        "update_url": update_url,
        "delete_url": delete_url,
        "cant_delete_msg": cant_delete_msg,
        "subtitle_emphasis": subtitle_emphasis,
    }


@register.inclusion_tag("frontpage/partials/list_group_item.html")
def list_group_item(value, date, update_url=None, delete_url=None):
    return {
        "value": value,
        "date": date,
        "update_url": update_url,
        "delete_url": delete_url,
    }


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
    """Creates a Bootstrap offcanvas toggle button.

    Usage:
    {% load components %}
    {% offcanvas_toggle "offcanvasWorkspace" "<i class='bi bi-collection'></i>" %}

    Parameters:
    - offcanvas_id: The ID of the offcanvas element (without the '#' prefix)
    - content: Optional HTML content for the toggle. Defaults to a collection icon.

    """

    cap_id = offcanvas_id.capitalize()

    html = f"""
<a id="offcanvas{cap_id}Toggle" data-bs-toggle="offcanvas" href="#offcanvas{cap_id}"
  role="button" aria-controls="offcanvas{cap_id}">
  {content}
</a>"""

    return mark_safe(html)


@register.simple_tag
def render_layout(card):
    if not isinstance(card, BaseLayout):
        raise TemplateSyntaxError("render_layout: you are trying to render a non-BaseLayout object.")
    return card.render()


@register.simple_tag
def nav_next(card):
    if isinstance(card, BasePrevNextNav):
        return card.render_next()
    return ""


@register.simple_tag
def nav_previous(card):
    if isinstance(card, BasePrevNextNav):
        return card.render_previous()
    return ""
