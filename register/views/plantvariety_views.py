from functools import cached_property
from typing import Any, Dict

from django_tables2 import RequestConfig

from breadcrumbs.generic.create import CreateBreadcrumbsMixin
from collect.models import SeedSample
from describe.models import Description
from django.core.paginator import Paginator
from django.db import models
from django.http import HttpRequest, HttpResponseBase
from django.shortcuts import get_object_or_404
from django.template.response import TemplateResponse
from django.urls.base import reverse_lazy
from django.views.generic import DetailView
from django.views.generic.edit import DeleteView, UpdateView
from breadcrumbs.decorators import list_breadcrumb
from parameters.models import VarietalParameter
from register.filters import PlantVarietyFilter
from register.forms import PlantVarietyForm
from register.models import PlantVariety, PlantVarietyName, Protection
from register.tables import (
    PlantVarietyAccessionTable,
    PlantVarietyDescriptionTable,
    ProtectionTable,
    VarietalParameterTable,
)
from register.views.base_views import NavActivePlants, custom_variety_crumbs
from register.views.plantspecies_views import PlantCreateMixin


class PlantVarietyCreate(CreateBreadcrumbsMixin, PlantCreateMixin):
    model = PlantVariety
    form_class = PlantVarietyForm


class PlantVarietyDetail(NavActivePlants, DetailView):
    model = PlantVariety
    context_object_name = "variety"

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        context = super().get_context_data(**kwargs)

        # The tables to display
        table_data = {
            "description_table": {"table": PlantVarietyDescriptionTable, "model": Description},
            "seedsample_table": {"table": PlantVarietyAccessionTable, "model": SeedSample},
            "protection_table": {"table": ProtectionTable, "model": Protection},
            "parameters_table": {"table": VarietalParameterTable, "model": VarietalParameter},
        }

        # Display the tables
        for key, value in table_data.items():
            table = value["table"](value["model"].objects.filter(variety=self.object.pk))
            RequestConfig(self.request, paginate={"per_page": 10}).configure(table)
            context[key] = table

        return context


class PlantVarietyUpdateView(NavActivePlants, UpdateView):
    model = PlantVariety
    fields = [
        "breeder",
    ]


class PlantVarietyDelete(NavActivePlants, DeleteView):
    model = PlantVariety

    def get_success_url(self):
        return reverse_lazy("register:variety_list", args=[self.object.species.pk])


class PlantVarietyNameCreate(PlantCreateMixin):
    model = PlantVarietyName
    fields = [
        "name",
        "change_date",
    ]

    def dispatch(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponseBase:
        self.variety = get_object_or_404(PlantVariety, pk=self.kwargs["pk"])
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["variety"] = self.variety
        return context

    def get_success_url(self):
        return reverse_lazy("register:plantvariety_detail", args=[self.kwargs["pk"]])

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.variety = self.variety
        self.object.save()
        return super().form_valid(form)


class PlantVarietyNameUpdate(NavActivePlants, UpdateView):
    model = PlantVarietyName
    fields = [
        "name",
        "change_date",
    ]

    def get_success_url(self):
        return reverse_lazy("register:plantvariety_detail", args=[self.object.variety.pk])


class PlantVarietyNameDelete(NavActivePlants, DeleteView):
    model = PlantVarietyName

    def get_success_url(self):
        return reverse_lazy("register:plantvariety_detail", args=[self.object.variety.pk])


def get_model_verbose_name_plural_capitalized(model: models.Model):
    return model._meta.verbose_name_plural.capitalize()


@list_breadcrumb(PlantVariety)
def plantvariety_list(request):
    view_func = request.resolver_match.func
    view_name = view_func.__name__

    # Optionally, get the fully qualified name (including module)
    full_view_name = f"{view_func.__module__}.{view_name}"

    print(f"Current view function: {view_name}")
    print(f"Full view function path: {full_view_name}")
    queryset = PlantVariety.objects.all().order_by("-created_at")
    flt = PlantVarietyFilter(request.GET, queryset=queryset)
    paginator = Paginator(flt.qs, 12)
    page = request.GET.get("page", 1)
    page_obj = paginator.page(page)

    return TemplateResponse(
        request,
        "register/plantvariety_list.html",
        {
            "filter": flt,
            "page_obj": page_obj,
        },
    )
