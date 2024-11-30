from django import template

register = template.Library()


@register.inclusion_tag("frontpage/partials/list_page_header.html")
def list_page_header(title, *args, **kwargs):
    return {"page_title": title, "create_url": kwargs["create_url"]}


@register.inclusion_tag("frontpage/partials/detail_page_header.html")
def detail_page_header(instance=None, title="", subtitle="", update_url=None, delete_url=None, **kwargs):
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
    }


@register.inclusion_tag("frontpage/partials/list_group_item.html")
def list_group_item(value, label, url="#", time=""):
    return {"value": value, "label": label, "url": url, "time": time}


@register.inclusion_tag("frontpage/partials/card_col_rows.html")
def card_col_rows(title, label, url="#", time=""):
    return {"title": title, "label": label, "url": url, "time": time}
