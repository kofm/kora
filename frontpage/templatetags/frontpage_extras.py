from django import template
from django.core.paginator import Paginator
from django.utils.html import format_html

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


@register.filter("add_suffix")
def add_suffix(value, suffix):
    if not isinstance(value, str):
        value = str(value)
    return f"{value}{suffix}"


@register.filter("italic")
def italic(value):
    if not isinstance(value, str):
        value = str(value)
    return format_html(f"<i>{value}</i>")
