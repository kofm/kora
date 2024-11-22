from django import template
from django.core.paginator import Paginator
from widget_tweaks.templatetags.widget_tweaks import silence_without_field, add_class

register = template.Library()


@register.simple_tag
def nav_css_class(page_class):
    if not page_class:
        return ""
    else:
        return page_class


@register.simple_tag
def get_proper_elided_page_range(p, number, on_each_side=3, on_ends=2):
    paginator = Paginator(p.object_list, p.per_page)
    return paginator.get_elided_page_range(number=number, on_each_side=on_each_side, on_ends=on_ends)


@register.inclusion_tag("frontpage/partials/edit_icon.html")
def render_edit_icon(url):
    return {"url": url}


@register.filter("add_valid_class")
@silence_without_field
def add_valid_class(field, css_class):
    if field.form.is_bound and not (hasattr(field, "errors") and field.errors):
        return add_class(field, css_class)
    return field


@register.filter("add_suffix")
def add_suffix(value, suffix):
    if not isinstance(value, str):
        value = str(value)
    return f"{value}{suffix}"
