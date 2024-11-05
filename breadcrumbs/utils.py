import re

from django.db.models.base import Model
from django.urls import reverse
from register.models import PlantVariety

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


def generate_breadcrumbs(request, model=None, object=None):
    crumbs = []
    url_name = get_view_url_name(request)
    if model:
        crumbs.append(list_crumb(model))
    if re.search("_create$", url_name):
        crumbs.append(create_crumb(model))
    if object:
        crumbs.append(detail_crumb(object))
        if re.search("_update$", url_name):
            crumbs.append(update_crumb(object))
        if re.search("_delete$", url_name):
            crumbs.append(delete_crumb(object))
    return {CONTEXT_KEY: crumbs}


def add_plantvariety_breadcrumbs(crumbs, plantvariety_object):
    return {CONTEXT_KEY: [list_crumb(PlantVariety), detail_crumb(plantvariety_object)] + crumbs[CONTEXT_KEY]}


def get_view_url_name(request):
    # ResolverMatch(func=register.views.plantvariety_views.plantvariety_list,
    # args=(), kwargs={}, url_name='variety_list',
    # app_names=['register'], namespaces=['register'],
    # route='varieties')
    return request.resolver_match.url_name
