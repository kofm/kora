from functools import cached_property
from typing import Any, Dict
from django.core.paginator import Paginator
from django.http import HttpRequest, HttpResponseBase
from django.shortcuts import get_object_or_404, render
from django_tables2 import RequestConfig


from collect.models import SeedSample
from django.urls.base import reverse_lazy
from django.views.generic import DetailView
from django.views.generic.edit import DeleteView, UpdateView
from describe.models import Description
from parameters.models import VarietalParameter
from register.filters import PlantVarietyFilter
from register.tables import (
    PlantVarietyAccessionTable,
    ProtectionTable,
    PlantVarietyDescriptionTable,
    VarietalParameterTable,
)
from view_breadcrumbs import BaseBreadcrumbMixin, CreateBreadcrumbMixin

from register.forms import PlantVarietyForm
from register.models import PlantSpecies, PlantVariety, PlantVarietyName, Protection
from register.views.base_views import (
    NavActivePlants,
    custom_variety_crumbs,
)
from register.views.plantspecies_views import PlantCreateMixin


class PlantVarietyCreate(PlantCreateMixin):
    model = PlantVariety
    form_class = PlantVarietyForm


class PlantVarietyDetail(NavActivePlants, BaseBreadcrumbMixin, DetailView):
    model = PlantVariety
    context_object_name = "variety"

    @cached_property
    def crumbs(self):
        return custom_variety_crumbs(self.object)

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


class PlantVarietyUpdateView(NavActivePlants, BaseBreadcrumbMixin, UpdateView):
    model = PlantVariety
    fields = [
        "breeder",
    ]

    @cached_property
    def crumbs(self):
        return custom_variety_crumbs(
            self.object,
            (f"Update: {self.object}", self.object.get_absolute_url()),
        )


class PlantVarietyDelete(NavActivePlants, DeleteView):
    model = PlantVariety

    def get_success_url(self):
        return reverse_lazy("register:plantspecies_detail", args=[self.object.species.pk])


class PlantVarietyNameCreate(BaseBreadcrumbMixin, PlantCreateMixin):
    model = PlantVarietyName
    fields = [
        "name",
        "change_date",
    ]

    @cached_property
    def crumbs(self):
        return custom_variety_crumbs(
            self.variety,
            (f"Add {self.model._meta.verbose_name.capitalize()}", ""),
        )

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


class PlantVarietyNameUpdate(NavActivePlants, BaseBreadcrumbMixin, UpdateView):
    model = PlantVarietyName
    fields = [
        "name",
        "change_date",
    ]

    @cached_property
    def crumbs(self):
        return custom_variety_crumbs(
            self.object.variety,
            (f"Update {self.model._meta.verbose_name.capitalize()}", ""),
        )

    def get_success_url(self):
        return reverse_lazy("register:plantvariety_detail", args=[self.object.variety.pk])


class PlantVarietyNameDelete(NavActivePlants, DeleteView):
    model = PlantVarietyName

    def get_success_url(self):
        return reverse_lazy("register:plantvariety_detail", args=[self.object.variety.pk])


def plantvariety_list(request):
    queryset = PlantVariety.objects.all().order_by("-created_at")
    filter = PlantVarietyFilter(request.GET, queryset=queryset)
    paginator = Paginator(filter.qs, 12)
    count = filter.qs.count()
    page_obj = paginator.page(request.GET.get("page", 1))
    get_params = request.GET.copy()
    if "page" in get_params:
        del get_params["page"]
    return render(
        request,
        "register/plantvariety_list.html",
        {"form": filter.form, "page_obj": page_obj, "get_params": get_params.urlencode(), "count": count},
    )
