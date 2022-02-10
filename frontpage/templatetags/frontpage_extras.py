from django import template

register = template.Library()

@register.simple_tag
def nav_css_class(page_class):
    if not page_class:
        return ""
    else:
        return page_class

