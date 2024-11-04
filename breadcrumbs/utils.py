from django.db.models.base import Model
from django.urls import reverse

CONTEXT_KEY = "KORA_BREADCRUMBS"


def model_verbose(model):
    return model._meta.verbose_name_plural.title()


def app_label(model):
    return model._meta.app_label


def model_label(model):
    return model._meta.verbose_name.replace(" ", "")


def view_url(model, action):
    url_name = f"{app_label(model)}:{model_label(model)}_{action}"
    if isinstance(model, Model):
        return reverse(url_name, args=[model.pk])
    return reverse(url_name)


def add_crumbs(context, crumbs: list):
    context[CONTEXT_KEY] = crumbs
    return context


def list_crumb(model):
    return (model_verbose(model), view_url(model, "list"))


def create_crumb(model):
    return ("Create", view_url(model, "create"))


def update_crumb(object):
    return ("Update", view_url(object, "update"))


def delete_crumb(object):
    return ("Delete", view_url(object, "delete"))


def detail_crumb(object):
    if hasattr(object, "get_absolute_url") and callable(getattr(object, "get_absolute_url")):
        view_url = object.get_absolute_url()
    else:
        view_url = view_url(object)
    return (object.__str__(), view_url)


def generate_breadcrumbs(model=None, object=None, create=False, update=False, delete=False):
    crumbs = []
    if model:
        crumbs.append(list_crumb(model))
    if create:
        crumbs.append(create_crumb(model))
    if object:
        crumbs.append(detail_crumb(object))
        if update:
            crumbs.append(update_crumb(object))
        if delete:
            crumbs.append(delete_crumb(object))
    return {CONTEXT_KEY: crumbs}
