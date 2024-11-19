from django import template

register = template.Library()


@register.inclusion_tag("frontpage/partials/page_header.html")
def page_header(title, *args, **kwargs):
    return {"page_title": title, "create_url": kwargs["create_url"]}
