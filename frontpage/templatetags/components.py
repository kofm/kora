from django import template

register = template.Library()


@register.inclusion_tag("frontpage/partials/list_page_header.html")
def list_page_header(title, *args, **kwargs):
    return {"page_title": title, "create_url": kwargs["create_url"]}


@register.inclusion_tag("frontpage/partials/detail_page_header.html")
def detail_page_header(title, **kwargs):
    update_url = kwargs.get("update_url")
    return {"page_title": title, "update_url": update_url}


@register.inclusion_tag("frontpage/partials/list_group_item.html")
def list_group_item(value, label, url="#", time=""):
    return {"value": value, "label": label, "url": url, "time": time}


@register.inclusion_tag("frontpage/partials/card_col_rows.html")
def card_col_rows(title, label, url="#", time=""):
    return {"title": title, "label": label, "url": url, "time": time}
