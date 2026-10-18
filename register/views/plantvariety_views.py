from django.contrib.auth.decorators import permission_required
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.core.exceptions import PermissionDenied
from django.core.paginator import Paginator
from django.db.models import Exists, F, OuterRef, Prefetch
from django.http import HttpResponseBadRequest
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
from frontpage.headers import DetailHeader, HeaderAction, ListHeader
from frontpage.utils.htmx import htmx_response_redirect, htmx_response_trigger_close_modal
from frontpage.views_decorators import (
    NavPlantActiveContext,
    htmx_render_partial,
    is_htmx,
    nav_plant_active_context,
    public_catalog_view,
)
from parameters.models import VarietalParameter
from register.filters import PlantVarietyCardsOrderForm, PlantVarietyFilter
from register.forms import PlantVarietyForm, PlantVarietyNameForm
from register.models import PlantVariety, PlantVarietyName, Protection
from register.tables import (
    PlantVarietyDescriptionTable,
    PlantVarietyNameTable,
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
@public_catalog_view("register.view_plantvariety")
def plantvariety_detail(request, pk):
    variety = get_object_or_404(PlantVariety.objects.select_related("species"), pk=pk)
    sections = {
        "descriptions": (
            PlantVarietyDescriptionTable,
            lambda: Description.objects.select_related("protocol", "label").filter(variety=pk),
        ),
        "samples": (PlantVarietySampleTable, lambda: Sample.objects.with_availability().filter(variety=pk)),
        "names": (PlantVarietyNameTable, lambda: variety.names.all()),
        "protections": (ProtectionTable, lambda: Protection.objects.filter(variety=pk)),
        "parameters": (
            VarietalParameterTable,
            lambda: VarietalParameter.objects.select_related("parameter").filter(variety=pk),
        ),
    }
    private_sections = {"samples": "collect.view_sample", "parameters": "parameters.view_varietalparameter"}
    partial = request.GET.get("partial") if is_htmx(request) else None
    if partial not in (*sections, "header"):
        partial = None
    tables = {}
    for section, (table_class, queryset) in sections.items():
        if partial and partial != section:
            continue
        if section in private_sections and not request.user.has_perm(private_sections[section]):
            if partial:
                raise PermissionDenied
            continue
        table = table_class(queryset(), prefix=f"{section}-", template_name="frontpage/partials/htmx_table.html")
        RequestConfig(request).configure(table)
        query = request.GET.copy()
        query["partial"] = section
        query[table.prefixed_page_field] = table.page.number
        table.refresh_url = f"{request.path}?{query.urlencode()}"
        tables[section] = table

    if partial in sections:
        return TemplateResponse(
            request, f"register/plantvariety_detail.html#{partial}", {"variety": variety, "tables": tables}
        )

    header = DetailHeader(
        request,
        variety,
        title=variety.name,
        subtitle=variety.species.common_name,
        show_id=True,
    )
    breadcrumbs = generate_breadcrumbs(request, PlantVariety, variety, skip_if_htmx=False)
    context = {
        "variety": variety, "tables": tables, "header": header, "header_partial": partial == "header", **breadcrumbs
    }
    template = "register/plantvariety_detail.html"
    return TemplateResponse(request, f"{template}#header" if partial == "header" else template, context)


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
            if is_htmx(request):
                return htmx_response_trigger_close_modal(["varietyNamesChanged"])
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
    context["object_to_create"] = "Denomination"
    template = "frontpage/modal_form.html" if is_htmx(request) else "frontpage/_create_form.html"
    return TemplateResponse(request, template, context)


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
            if is_htmx(request):
                return htmx_response_trigger_close_modal(["varietyNamesChanged"])
            return redirect(reverse_lazy("register:variety_detail", args=[instance.variety.pk]))
    else:
        form = PlantVarietyNameForm(instance=instance)
    context["form"] = form
    context["object"] = instance
    context["instance"] = instance
    template = "frontpage/modal_form.html" if is_htmx(request) else "frontpage/_update_form.html"
    return TemplateResponse(request, template, context)


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
        if not instance.is_deletable():
            return HttpResponseBadRequest("The last denomination cannot be deleted.")
        instance.delete()
        if is_htmx(request):
            return htmx_response_trigger_close_modal(["varietyNamesChanged"])
        return redirect(reverse_lazy("register:variety_detail", args=[instance.variety.pk]))
    context["instance"] = instance
    template = (
        "frontpage/modal_confirm_delete.html" if is_htmx(request) else "register/plantvarietyname_confirm_delete.html"
    )
    return TemplateResponse(request, template, context)


@nav_plant_active_context
@public_catalog_view("register.view_plantvariety")
@htmx_render_partial("cards")
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

    actions = []
    actions.append(
        HeaderAction(
            label="Import Varieties",
            url=reverse("restapi:plantvariety-spreadsheet-import"),
            permission="register.add_plantvariety",
        )
    )
    header = ListHeader(request, PlantVariety, modal=True, actions=actions)

    context = {
        "filter": flt,
        "page_obj": page_obj,
        "order_form": order_form,
        **generate_breadcrumbs(request, PlantVariety),
        "header": header,
    }

    return TemplateResponse(request, "register/plantvariety_list.html", context)
