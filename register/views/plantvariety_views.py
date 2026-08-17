from django.contrib.auth.decorators import permission_required
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.core.paginator import Paginator
from django.db.models import Exists, F, OuterRef, Prefetch
from django.shortcuts import get_object_or_404, redirect
from django.template.response import TemplateResponse
from django.urls import reverse
from django.urls.base import reverse_lazy
from django_tables2 import RequestConfig

from breadcrumbs.generic import (
    CrumbsDeleteView,
)
from breadcrumbs.utils import (
    breadcrumbs_context,
    delete_breadcrumb,
    detail_breadcrumb,
    generate_breadcrumbs,
    list_breadcrumb,
    update_breadcrumb,
)
from calculator.models import Crop
from collect.models import Sample
from describe.models import Description
from frontpage.headers import DetailHeader
from frontpage.utils.htmx import htmx_response_redirect
from frontpage.views_decorators import NavPlantActiveContext, htmx_render_blocks, nav_plant_active_context
from parameters.models import VarietalParameter
from register.filters import PlantVarietyCardsOrderForm, PlantVarietyFilter
from register.forms import PlantVarietyForm, PlantVarietyNameForm
from register.models import PlantVariety, PlantVarietyName, Protection
from register.tables import (
    PlantVarietyDescriptionTable,
    PlantVarietySampleTable,
    ProtectionTable,
    VarietalParameterTable,
)


@nav_plant_active_context
@permission_required(["register.add_plantvariety"], raise_exception=True)
def plantvariety_create(request):
    form = PlantVarietyForm(request.POST or None)
    if form.is_valid():
        instance = form.save()
        return htmx_response_redirect(reverse("register:variety_detail", args=(instance.pk,)))
    context = {"form": form, "object_to_create": "Variety"}
    return TemplateResponse(request, "frontpage/modal_form.html", context)


@nav_plant_active_context
def plantvariety_detail(request, pk):
    variety = PlantVariety.objects.select_related("species").get(pk=pk)

    tables = {}
    descriptions = Description.objects.select_related("protocol", "label").filter(variety=pk)
    tables["description"] = PlantVarietyDescriptionTable(descriptions)
    samples = Sample.objects.with_availability().filter(variety=pk)
    tables["sample"] = PlantVarietySampleTable(samples)
    protections = Protection.objects.filter(variety=pk)
    tables["protection"] = ProtectionTable(protections)
    parameters = VarietalParameter.objects.select_related("parameter").filter(variety=pk)
    tables["parameter"] = VarietalParameterTable(parameters)

    req_config = RequestConfig(request)
    for key in tables:
        req_config.configure(tables[key])

    header = DetailHeader(
        request,
        variety,
        title=variety.name,
        subtitle=variety.species.common_name,
        show_id=True,
    )
    breadcrumbs = generate_breadcrumbs(request, PlantVariety, variety)
    context = {"variety": variety, "tables": tables, "header": header, **breadcrumbs}
    return TemplateResponse(request, "register/plantvariety_detail.html", context)


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
    breadcrumbs = [
        list_breadcrumb(PlantVariety),
        detail_breadcrumb(instance.variety),
        ("Denominations", f"{instance.variety.get_absolute_url()}#names"),
        detail_breadcrumb(instance),
        delete_breadcrumb(instance),
    ]
    context = {"object": instance, **breadcrumbs_context(breadcrumbs)}
    if request.method == "POST":
        instance.delete()
        return redirect(reverse_lazy("register:variety_detail", args=[instance.variety.pk]))
    return TemplateResponse(request, "register/plantvarietyname_confirm_delete.html", context)


@nav_plant_active_context
@htmx_render_blocks(["cards"])
def plantvariety_list(request):
    queryset = PlantVariety.objects.all()
    order_form = PlantVarietyCardsOrderForm(request.GET or None)
    ordering = "-created_at"
    if order_form.is_valid():
        ordering = order_form.save()
    queryset = queryset.order_by(ordering)
    flt = PlantVarietyFilter(request.GET, queryset=queryset)

    paginator = Paginator(flt.qs, 12)
    page_obj = paginator.get_page(request.GET.get("page"))

    prefetch_names = Prefetch(
        "names",
        queryset=PlantVarietyName.objects.exclude(name=F("variety__name")),
    )

    page_obj.object_list = (
        page_obj.object_list.select_related("species")
        .prefetch_related(prefetch_names)
        .annotate(
            has_descriptions=Exists(Description.objects.filter(variety=OuterRef("pk"))),
            has_samples=Exists(Sample.objects.filter(variety=OuterRef("pk"))),
            has_parameters=Exists(VarietalParameter.objects.filter(variety=OuterRef("pk"))),
            has_crops=Exists(Crop.objects.filter(variety=OuterRef("pk"))),
            has_protections=Exists(Protection.objects.filter(variety=OuterRef("pk"))),
        )
    )

    context = {
        "filter": flt,
        "page_obj": page_obj,
        "order_form": order_form,
        **generate_breadcrumbs(request, PlantVariety),
    }

    return TemplateResponse(request, "register/plantvariety_list.html", context)
