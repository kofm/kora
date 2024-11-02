from django.urls import reverse

CONTEXT_KEY = "KORA_BREADCRUMBS"


def model_verbose(model):
    return model._meta.verbose_name_plural.title()


def app_label(model):
    return model._meta.app_label


def model_label(model):
    return model._meta.verbose_name.replace(" ", "")


def view_url(model, action):
    return reverse(f"{app_label(model)}:{model_label(model)}_{action}")


def add_crumbs(context, crumbs: list):
    context[CONTEXT_KEY] = crumbs
    return context


def list_crumb(model):
    return (model_verbose(model), view_url(model, "list"))


def create_crumb(model):
    return ("Create", view_url(model, "create"))


def update_crumb(object):
    return ("Update", object.get_update_url() or None)


def detail_crumb(object):
    return (object.__str__(), object.get_absolute_url() or None)
