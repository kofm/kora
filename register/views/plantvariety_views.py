from typing import Any, Dict

from django_tables2 import RequestConfig

from breadcrumbs.decorators import list_breadcrumb
from breadcrumbs.generic import (
    CrumbsCreateView,
    CrumbsDeleteView,
    CrumbsDetailView,
    CrumbsUpdateView,
)
from breadcrumbs.utils import generate_breadcrumbs
from collect.models import SeedSample
from describe.models import Description
from django.core.paginator import Paginator
from django.db import models
from django.http import HttpRequest, HttpResponseBase
from django.shortcuts import get_object_or_404
from django.template.response import TemplateResponse
from django.urls.base import reverse_lazy
from frontpage.views_decorators import NavPlantActiveContext
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


class PlantVarietyCreate(NavPlantActiveContext, CrumbsCreateView):
    model = PlantVariety
    form_class = PlantVarietyForm
    template_name_suffix = "_create_form"

    def get_context_data(self, **kwargs):
        kwargs.update({"model_name": self.model._meta.verbose_name.title()})
        return super().get_context_data(**kwargs)


class PlantVarietyDetail(NavPlantActiveContext, CrumbsDetailView):
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


class PlantVarietyUpdateView(NavPlantActiveContext, CrumbsUpdateView):
    model = PlantVariety
    fields = ["breeder"]
    template_name = "register/plantvariety_update_form.html"


class PlantVarietyDelete(NavPlantActiveContext, CrumbsDeleteView):
    model = PlantVariety

    def get_success_url(self):
        return reverse_lazy("register:variety_list")


class PlantVarietyNameCreate(CrumbsCreateView):
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


class PlantVarietyNameUpdate(NavPlantActiveContext, CrumbsUpdateView):
    model = PlantVarietyName
    fields = [
        "name",
        "change_date",
    ]

    def get_success_url(self):
        return reverse_lazy("register:plantvariety_detail", args=[self.object.variety.pk])


class PlantVarietyNameDelete(NavPlantActiveContext, CrumbsDeleteView):
    model = PlantVarietyName

    def get_success_url(self):
        return reverse_lazy("register:plantvariety_detail", args=[self.object.variety.pk])


def get_model_verbose_name_plural_capitalized(model: models.Model):
    return model._meta.verbose_name_plural.capitalize()


def plantvariety_list(request):
    queryset = PlantVariety.objects.all().order_by("-created_at")
    flt = PlantVarietyFilter(request.GET, queryset=queryset)
    paginator = Paginator(flt.qs, 12)
    page = request.GET.get("page", 1)
    page_obj = paginator.page(page)
    context = {"filter": flt, "page_obj": page_obj}
    context.update(generate_breadcrumbs(request, PlantVariety))
    return TemplateResponse(
        request,
        "register/plantvariety_list.html",
        context,
    )
