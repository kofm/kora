from django.contrib import messages
from django.contrib.auth.decorators import permission_required
from django.db.models import Count
from django.db.models.deletion import ProtectedError
from django.shortcuts import get_object_or_404, redirect
from django.template.response import TemplateResponse
from django.urls import reverse
from django.views.decorators.http import require_POST
from django_tables2 import RequestConfig

from breadcrumbs.utils import add_parent_breadcrumbs, breadcrumbs_context, generate_breadcrumbs
from calculator.filters import CropLayoutFilter
from calculator.forms import CropLayoutForm, CropModelForm, InLocationCropLayoutForm, ManagementForm
from calculator.layouts import CropSortableGrid, FieldBookCardLayout
from calculator.models import CropLayout
from calculator.tables import CropLayoutListTable
from frontpage.headers import ArchivalDetailHeader, HeaderAction, ListHeader
from frontpage.utils.assets import add_layout_assets
from frontpage.utils.htmx import htmx_response_redirect, htmx_response_trigger_close_modal
from frontpage.views_decorators import htmx_render_blocks, is_htmx, nav_active
from spaces.models import Location

LAYOUT_DETAIL_TABS = {"crops", "fieldbooks", "management"}


@permission_required("calculator.view_croplayout", raise_exception=True)
@nav_active("nav_plan")
@htmx_render_blocks(["main"])
def layout_list(request):
    queryset = CropLayout.objects.select_related("location").annotate(
        crop_count=Count("crops", distinct=True),
        fieldbook_count=Count("fieldbooks", distinct=True),
    )
    layout_filter = CropLayoutFilter(request.GET, queryset=queryset)
    table = CropLayoutListTable(layout_filter.qs)
    RequestConfig(request, paginate={"per_page": 15}).configure(table)
    header = ListHeader(request, CropLayout, modal=True)
    context = {
        "filter": layout_filter,
        "table": table,
        "header": header,
        **breadcrumbs_context([("Crop layouts", reverse("calculator:croplayout_list"))]),
    }
    return TemplateResponse(request, "calculator/layout_list.html", context)


@permission_required("calculator.view_croplayout", raise_exception=True)
def layout_detail(request, pk):
    layout = get_object_or_404(CropLayout.objects.select_related("location"), pk=pk)
    active_tab = request.GET.get("tab", "crops")
    if active_tab not in LAYOUT_DETAIL_TABS:
        active_tab = "crops"

    crops = list(layout.crops.select_related("variety__species").order_by("order", "pk"))
    crop_cards = CropSortableGrid(
        crops,
        num_columns=layout.ncol,
        sort_view="calculator:crop_sort",
        is_sortable=False,
        is_read_only=layout.is_archived,
    )
    fieldbook_cards = FieldBookCardLayout(layout.fieldbooks.all())
    actions = []
    if not layout.is_archived:
        actions.append(
            HeaderAction(
                label="Import Crops",
                url=reverse("restapi:crops-excel-import"),
                permission="calculator.add_crop",
            )
        )
    actions.append(
        HeaderAction(
            label="Delete",
            url=reverse("calculator:layout_delete", args=[layout.pk]),
            permission="calculator.delete_croplayout",
            modal=True,
            disabled=not layout.is_deletable,
            disabled_message=layout.cant_delete_msg,
        )
    )

    header = ArchivalDetailHeader(
        request,
        layout,
        subtitle=layout.location,
        update_modal=True,
        show_id=True,
        actions=actions,
    )

    breadcrumbs = add_parent_breadcrumbs(generate_breadcrumbs(request, CropLayout, layout), layout.location)
    context = {
        "layout": layout,
        "active_tab": active_tab,
        "crop_cards": crop_cards,
        "crop_count": len(crops),
        "fieldbook_cards": fieldbook_cards,
        "managements": layout.managements.select_related("type").order_by("date"),
        "is_read_only": layout.is_archived,
        "header": header,
        **breadcrumbs,
    }
    add_layout_assets(context, crop_cards)
    template_name = "calculator/layout_detail.html#active_tab" if is_htmx(request) else "calculator/layout_detail.html"
    return TemplateResponse(request, template_name, context)


@permission_required("calculator.add_croplayout", raise_exception=True)
def layout_create(request):
    form = CropLayoutForm(request.POST or None)
    if form.is_valid():
        form.save()
        if is_htmx(request):
            return htmx_response_trigger_close_modal(["resultsChanged"])
    return TemplateResponse(request, "frontpage/modal_form.html", {"form": form, "object_to_create": "Crop layout"})


@permission_required("calculator.add_croplayout", raise_exception=True)
def location_layout_create(request, location_id):
    location = get_object_or_404(Location, pk=location_id)
    form = InLocationCropLayoutForm(request.POST or None)
    if form.is_valid():
        layout = form.save(commit=False)
        layout.location = location
        layout.save()
        return redirect(layout)
    return TemplateResponse(request, "frontpage/_create_form.html", {"form": form, "model_name": "Crop layout"})


@permission_required("calculator.change_croplayout", raise_exception=True)
def layout_update(request, pk):
    layout = get_object_or_404(CropLayout.objects.visible().select_related("location"), pk=pk)
    form = InLocationCropLayoutForm(request.POST or None, instance=layout)
    if form.is_valid():
        form.save()
        if is_htmx(request):
            return htmx_response_redirect(layout.get_absolute_url())
        return redirect(layout)
    template_name = "frontpage/modal_form.html" if is_htmx(request) else "frontpage/_update_form.html"
    return TemplateResponse(request, template_name, {"form": form, "instance": layout, "object": layout})


@permission_required("calculator.add_crop", raise_exception=True)
def layout_crop_create(request, layout_id):
    layout = get_object_or_404(CropLayout.objects.visible(), pk=layout_id)
    form = CropModelForm(request.POST or None)
    form.fields.pop("layout")
    if form.is_valid():
        crop = form.save(commit=False)
        crop.layout = layout
        crop.save()
        if is_htmx(request):
            return htmx_response_trigger_close_modal(["cropsUpdated"])
        return redirect(layout)
    template_name = "frontpage/modal_form.html" if is_htmx(request) else "frontpage/_create_form.html"
    return TemplateResponse(
        request,
        template_name,
        {"form": form, "model_name": "Crop", "object_to_create": "Crop"},
    )


@permission_required("calculator.add_management", raise_exception=True)
def layout_management_create(request, layout_id):
    layout = get_object_or_404(CropLayout.objects.visible(), pk=layout_id)
    form = ManagementForm(request.POST or None)
    if form.is_valid():
        management = form.save(commit=False)
        management.layout = layout
        management.save()
        if is_htmx(request):
            return htmx_response_trigger_close_modal(["managementsUpdated"])
        return redirect(layout)
    template_name = "frontpage/modal_form.html" if is_htmx(request) else "frontpage/_create_form.html"
    return TemplateResponse(
        request,
        template_name,
        {"form": form, "model_name": "Management", "object_to_create": "Management"},
    )


@require_POST
@permission_required("calculator.change_croplayout", raise_exception=True)
def layout_archive(request, pk):
    layout = get_object_or_404(CropLayout.objects.visible(), pk=pk)
    layout.archive()
    if is_htmx(request):
        return htmx_response_redirect(layout.get_absolute_url())
    return redirect(layout)


@require_POST
@permission_required("calculator.change_croplayout", raise_exception=True)
def layout_restore(request, pk):
    layout = get_object_or_404(CropLayout.objects.archived(), pk=pk)
    layout.restore()
    if is_htmx(request):
        return htmx_response_redirect(layout.get_absolute_url())
    return redirect(layout)


@permission_required("calculator.delete_croplayout", raise_exception=True)
def layout_delete(request, pk):
    layout = get_object_or_404(CropLayout.objects.select_related("location"), pk=pk)
    if request.method == "POST":
        try:
            layout.delete()
        except ProtectedError:
            messages.error(request, layout.cant_delete_msg)
            redirect_url = layout.get_absolute_url()
        else:
            redirect_url = reverse("calculator:croplayout_list")

        if is_htmx(request):
            return htmx_response_redirect(redirect_url)
        return redirect(redirect_url)
    template_name = "frontpage/modal_confirm_delete.html" if is_htmx(request) else "frontpage/confirm_delete.html"
    return TemplateResponse(request, template_name, {"instance": layout, "object": layout})
