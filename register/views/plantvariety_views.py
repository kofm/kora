from django.contrib.auth.decorators import permission_required
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404, redirect
from django.template.response import TemplateResponse
from django.urls import reverse
from django.urls.base import reverse_lazy
from django_tables2 import RequestConfig

from breadcrumbs.generic import (
    CrumbsCreateView,
    CrumbsDeleteView,
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
from collect.models import Sample
from describe.models import Description
from frontpage.views_decorators import NavPlantActiveContext, nav_plant_active_context
from parameters.models import VarietalParameter
from register.filters import PlantVarietyFilter
from register.forms import PlantVarietyForm, PlantVarietyNameForm
from register.models import PlantVariety, PlantVarietyName, Protection
from register.tables import (
    PlantVarietyDescriptionTable,
    PlantVarietySampleTable,
    ProtectionTable,
    VarietalParameterTable,
)


class PlantVarietyCreate(PermissionRequiredMixin, NavPlantActiveContext, CrumbsCreateView):
    model = PlantVariety
    form_class = PlantVarietyForm
    template_name = "frontpage/_create_form.html"
    permission_required = ["register.add_plantvariety"]

    def get_context_data(self, **kwargs):
        kwargs.update({"model_name": self.model._meta.verbose_name.title()})
        return super().get_context_data(**kwargs)


@nav_plant_active_context
def plantvariety_detail(request, pk):
    variety = PlantVariety.objects.select_related("species").get(pk=pk)
    context = {"variety": variety}

    tables = {}
    descriptions = Description.objects.with_expressions().filter(variety=pk)
    tables["description"] = PlantVarietyDescriptionTable(descriptions)
    samples = Sample.objects.with_availability().filter(variety=pk)
    tables["sample"] = PlantVarietySampleTable(samples)
    protections = Protection.objects.filter(variety=pk)
    tables["protection"] = ProtectionTable(protections)
    parameters = VarietalParameter.objects.select_related("parameter").filter(variety=pk)
    tables["parameter"] = VarietalParameterTable(parameters)

    for key in tables:
        RequestConfig(request).configure(tables[key])

    context["tables"] = tables
    context.update(generate_breadcrumbs(request, PlantVariety, variety))
    return TemplateResponse(request, "register/plantvariety_detail.html", context)


class PlantVarietyUpdateView(PermissionRequiredMixin, NavPlantActiveContext, CrumbsUpdateView):
    model = PlantVariety
    fields = ("breeder",)
    template_name = "register/plantvariety_update_form.html"
    permission_required = ["register.change_plantvariety"]


class PlantVarietyDelete(PermissionRequiredMixin, NavPlantActiveContext, CrumbsDeleteView):
    object: PlantVariety
    model = PlantVariety
    permission_required = ["register.delete_plantvariety"]

    def get_success_url(self):
        return reverse_lazy("register:variety_list")


@permission_required("register.add_plantvarietyname", raise_exception=True)
def plantvarietyname_create(request, pk):
    context = {}
    variety = get_object_or_404(PlantVariety, pk=pk)
    if request.method == "POST":
        form = PlantVarietyNameForm(request.POST)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.variety = variety
            instance.save()
            return redirect(reverse("register:variety_detail", args=[pk]))
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


@permission_required("register.change_plantvarietyname", raise_exception=True)
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
            return redirect(reverse_lazy("register:variety_detail", args=[instance.variety.pk]))
    else:
        form = PlantVarietyNameForm(instance=instance)
    context["form"] = form
    context["object"] = instance
    return TemplateResponse(request, "frontpage/_update_form.html", context)


@permission_required("register.delete_plantvarietyname", raise_exception=True)
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
        return redirect(reverse_lazy("register:variety_detail", args=[instance.variety.pk]))
    return TemplateResponse(request, "register/plantvarietyname_confirm_delete.html", context)


@nav_plant_active_context
def plantvariety_list(request):
    queryset = (
        PlantVariety.objects.prefetch_related(
            "names",
            "description_set",
            "sample_set",
            "parameters",
            "crop_set",
            "protection_set",
        )
        .select_related("species", "breeder")
        .all()
        .order_by("-created_at")
        .distinct()
    )
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
