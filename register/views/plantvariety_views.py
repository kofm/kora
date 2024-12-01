from typing import TYPE_CHECKING, Any

from django_tables2 import RequestConfig

from breadcrumbs.generic import (
    CrumbsCreateView,
    CrumbsDeleteView,
    CrumbsDetailView,
    CrumbsUpdateView,
)
from breadcrumbs.utils import (
    breadcrumbs_context,
    delete_breadcrumb,
    detail_breadcrumb,
    generate_breadcrumbs,
    list_breadcrumb,
    update_breadcrumb,
)
from collect.models import SeedSample
from describe.models import Description
from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404, redirect
from django.template.response import TemplateResponse
from django.urls import reverse
from django.urls.base import reverse_lazy
from frontpage.views_decorators import NavPlantActiveContext, nav_plant_active_context
from parameters.models import VarietalParameter
from register.filters import PlantVarietyFilter
from register.forms import PlantVarietyForm, PlantVarietyNameForm
from register.models import PlantVariety, PlantVarietyName, Protection
from register.tables import (
    PlantVarietyAccessionTable,
    PlantVarietyDescriptionTable,
    ProtectionTable,
    VarietalParameterTable,
)

if TYPE_CHECKING:
    from django_tables2.tables import Table

    from django.models import Model


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

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        # The tables to display

        table_data: dict[str, dict[str, Table | Model]] = {
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
    fields = ("breeder",)
    template_name = "register/plantvariety_update_form.html"


class PlantVarietyDelete(NavPlantActiveContext, CrumbsDeleteView):
    object: PlantVariety
    model = PlantVariety

    def get_success_url(self):
        return reverse_lazy("register:variety_list")


def plantvarietyname_create(request, pk):
    context = {}
    variety = get_object_or_404(PlantVariety, pk=pk)
    if request.method == "POST":
        form = PlantVarietyNameForm(request.POST)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.variety = variety
            instance.save()
            return redirect(reverse("register:plantvariety_detail", args=[pk]))
    else:
        form = PlantVarietyNameForm()
    breadcrumbs = [
        list_breadcrumb(PlantVariety),
        detail_breadcrumb(variety),
        ("Denominations", f"{variety.get_absolute_url()}#names"),
        ("Create", ""),
    ]
    context["form"] = form
    context["model_name"] = "Denomination"
    context.update(breadcrumbs_context(breadcrumbs))
    return TemplateResponse(request, "frontpage/_create_form.html", context)


def plantvarietyname_update(request, pk):
    context = {}
    instance = get_object_or_404(PlantVarietyName, pk=pk)
    breadcrumbs = [
        list_breadcrumb(PlantVariety),
        detail_breadcrumb(instance.variety),
        ("Denominations", f"{instance.variety.get_absolute_url()}#names"),
        update_breadcrumb(instance),
    ]
    context.update(breadcrumbs_context(breadcrumbs))
    if request.method == "POST":
        form = PlantVarietyNameForm(request.POST, instance=instance)
        if form.is_valid():
            form.save()
            return redirect(reverse_lazy("register:plantvariety_detail", args=[instance.variety.pk]))
    else:
        form = PlantVarietyNameForm(instance=instance)
    context["form"] = form
    context["object"] = instance
    return TemplateResponse(request, "frontpage/_update_form.html", context)


def plantvarietyname_delete(request, pk):
    instance = get_object_or_404(PlantVarietyName, pk=pk)
    context = {"object": instance}
    breadcrumbs = [
        list_breadcrumb(PlantVariety),
        detail_breadcrumb(instance.variety),
        ("Denominations", f"{instance.variety.get_absolute_url()}#names"),
        detail_breadcrumb(instance),
        delete_breadcrumb(instance),
    ]
    context.update(breadcrumbs_context(breadcrumbs))
    if request.method == "POST":
        instance.delete()
        return redirect(reverse_lazy("register:plantvariety_detail", args=[instance.variety.pk]))
    return TemplateResponse(request, "register/plantvarietyname_confirm_delete.html", context)


@nav_plant_active_context
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
