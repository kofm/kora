from typing import Any, Dict, List, Optional, Tuple, Type

from django.db.models.base import Model
from django.http import HttpRequest
from django.urls import reverse
from register.models import PlantVariety

Breadcrumb = Tuple[str, str]
BreadcrumbList = List[Breadcrumb]
BreadcrumbContext = Dict[str, BreadcrumbList]

CONTEXT_KEY = "KORA_BREADCRUMBS"


def breadcrumbs_context(breadcrumbs: BreadcrumbList) -> BreadcrumbContext:
    return {CONTEXT_KEY: breadcrumbs}


def model_verbose(model: Type[Model]) -> str:
    return model._meta.verbose_name_plural.title()


def model_name(model: Type[Model]) -> str:
    return model._meta.verbose_name.replace(" ", "")


def app_label(model: Type[Model]) -> str:
    return model._meta.app_label


def view_url(model: Type[Model], action: str) -> str:
    url_name = f"{app_label(model)}:{model_name(model)}_{action}"
    if isinstance(model, Model):
        return reverse(url_name, args=[model.pk])
    return reverse(url_name)


def get_view_url_name(request: HttpRequest) -> str:
    return request.resolver_match.url_name


def list_breadcrumb(model: Type[Model]) -> tuple[str, str]:
    return (model_verbose(model), view_url(model, "list"))


def create_breadcrumb(model: Type[Model]) -> tuple[str, str]:
    return ("Create", view_url(model, "create"))


def update_breadcrumb(instance: Model) -> tuple[str, str]:
    return ("Update", view_url(instance, "update"))


def delete_breadcrumb(instance: Model) -> tuple[str, str]:
    return ("Delete", view_url(instance, "delete"))


def detail_breadcrumb(instance: Model) -> tuple[str, str]:
    if hasattr(instance, "get_absolute_url") and callable(getattr(instance, "get_absolute_url")):
        view_url = instance.get_absolute_url()
    else:
        view_url = view_url(instance)
    return (instance.__str__(), view_url)


def add_breadcrumbs(context: Dict[str, Any], crumbs: BreadcrumbList) -> Dict[str, Any]:
    context[CONTEXT_KEY] = crumbs
    return context


def generate_breadcrumbs(
    request: HttpRequest, model: Optional[Type[Model]] = None, instance: Optional[Model] = None
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

    return breadcrumbs_context(breadcrumbs)


def add_plantvariety_breadcrumbs(breadcrumbs: BreadcrumbList, plantvariety_instance: PlantVariety) -> BreadcrumbContext:
    plantvariety_breadcrumbs = [list_breadcrumb(PlantVariety), detail_breadcrumb(plantvariety_instance)]
    return breadcrumbs_context(plantvariety_breadcrumbs + breadcrumbs[CONTEXT_KEY])
