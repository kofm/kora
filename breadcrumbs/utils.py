from typing import Any, Union

from django.db.models.base import Model
from django.http import HttpRequest
from django.urls import NoReverseMatch, reverse

from register.models import PlantVariety

Breadcrumb = tuple[str, str]
BreadcrumbList = list[Breadcrumb]
BreadcrumbContext = dict[str, BreadcrumbList]

CONTEXT_KEY = "KORA_BREADCRUMBS"


def breadcrumbs_context(breadcrumbs: BreadcrumbList) -> BreadcrumbContext:
    return {CONTEXT_KEY: breadcrumbs}


def model_verbose(model: Union[Model, type[Model]]) -> str:
    verbose_name_plural = str(model._meta.verbose_name_plural)
    return verbose_name_plural.title()


def model_name(model: Union[Model, type[Model]]) -> str:
    verbose_name = model._meta.verbose_name
    if isinstance(verbose_name, str):
        return verbose_name.replace(" ", "")
    return ""


def app_label(model: Union[Model, type[Model]]) -> str:
    return model._meta.app_label


def view_url(model: Union[Model, type[Model]], action: str) -> str:
    url_name = f"{app_label(model)}:{model_name(model)}_{action}"
    try:
        if isinstance(model, Model):
            url = reverse(url_name, args=[model.pk])
        else:
            url = reverse(url_name)
        return url
    except NoReverseMatch:
        return ""


def get_view_url_name(request: HttpRequest) -> str:
    if isinstance(request, HttpRequest) and request.resolver_match:
        url_name = request.resolver_match.url_name
        if url_name is None:
            e = "Expected url_name to be a string, got None"
            raise ValueError(e)
        return url_name
    e = "Invalid request: Not an instance of HttpRequest or missing resolver_match"
    raise ValueError(e)


def list_breadcrumb(model: type[Model]) -> tuple[str, str]:
    return (model_verbose(model), view_url(model, "list"))


def create_breadcrumb(model: type[Model]) -> tuple[str, str]:
    return ("Create", view_url(model, "create"))


def update_breadcrumb(instance: Model) -> tuple[str, str]:
    return ("Update", view_url(instance, "update"))


def delete_breadcrumb(instance: Model) -> tuple[str, str]:
    return ("Delete", view_url(instance, "delete"))


def detail_breadcrumb(instance: Model) -> tuple[str, str]:
    if hasattr(instance, "get_absolute_url"):
        url = instance.get_absolute_url()  # type: ignore[reportAttributeAccessIssue]
    else:
        url = view_url(instance, "detail")
    return (str(instance), url)


def add_breadcrumbs(context: dict[str, Any], crumbs: BreadcrumbList) -> dict[str, Any]:
    context[CONTEXT_KEY] = crumbs
    return context


def generate_breadcrumbs(
    request: HttpRequest,
    model: type[Model] | None = None,
    instance: Model | None = None,
    additional: BreadcrumbList | None = None,
) -> BreadcrumbContext:
    breadcrumbs = []
    url_name = get_view_url_name(request)

    if model:
        breadcrumbs.append(list_breadcrumb(model))

    if model and url_name.endswith("_create"):
        breadcrumbs.append(create_breadcrumb(model))

    if instance:
        breadcrumbs.append(detail_breadcrumb(instance))

    if instance and url_name.endswith("_update"):
        breadcrumbs.append(update_breadcrumb(instance))

    if instance and url_name.endswith("_delete"):
        breadcrumbs.append(delete_breadcrumb(instance))

    if additional:
        breadcrumbs = breadcrumbs + additional

    return breadcrumbs_context(breadcrumbs)


def add_plantvariety_breadcrumbs(
    breadcrumbs: BreadcrumbContext, plantvariety_instance: PlantVariety
) -> BreadcrumbContext:
    plantvariety_breadcrumbs = [list_breadcrumb(PlantVariety), detail_breadcrumb(plantvariety_instance)]
    return breadcrumbs_context(plantvariety_breadcrumbs + breadcrumbs[CONTEXT_KEY])
