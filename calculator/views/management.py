from django.contrib import messages
from django.contrib.auth.decorators import permission_required
from django.db.models.deletion import ProtectedError
from django.shortcuts import get_object_or_404, redirect
from django.template.response import TemplateResponse
from django_tables2 import RequestConfig

from breadcrumbs.utils import generate_breadcrumbs
from calculator.filters import ManagementTypeFilter
from calculator.forms import ManagementTypeForm
from calculator.models import ManagementType
from calculator.tables import ManagementTypeTable
from frontpage.headers import ListHeader
from frontpage.utils.htmx import htmx_response_trigger_close_modal
from frontpage.views_decorators import htmx_render_blocks, is_htmx, nav_active


@permission_required("calculator.view_managementtype", raise_exception=True)
@nav_active("nav_plan")
@htmx_render_blocks(["main"])
def managementtype_list(request):
    managementtype_filter = ManagementTypeFilter(request.GET, queryset=ManagementType.objects.all())
    table = ManagementTypeTable(managementtype_filter.qs)
    RequestConfig(request, paginate={"per_page": 15}).configure(table)
    context = {
        "filter": managementtype_filter,
        "table": table,
        "header": ListHeader(request, ManagementType, title="Operations", subtitle="Management", modal=True),
        **generate_breadcrumbs(request, ManagementType),
    }
    return TemplateResponse(request, "calculator/managementtype_list.html", context)


@permission_required("calculator.add_managementtype", raise_exception=True)
def managementtype_create(request):
    form = ManagementTypeForm(request.POST or None)
    if form.is_valid():
        form.save()
        if is_htmx(request):
            return htmx_response_trigger_close_modal(["resultsChanged"])
        return redirect("calculator:managementtype_list")
    return TemplateResponse(
        request,
        "frontpage/modal_form.html",
        {"form": form, "object_to_create": "management type"},
    )


@permission_required("calculator.change_managementtype", raise_exception=True)
def managementtype_update(request, pk):
    management_type = get_object_or_404(ManagementType, pk=pk)
    form = ManagementTypeForm(request.POST or None, instance=management_type)
    if form.is_valid():
        form.save()
        if is_htmx(request):
            return htmx_response_trigger_close_modal(["resultsChanged"])
        return redirect("calculator:managementtype_list")
    return TemplateResponse(
        request,
        "frontpage/modal_form.html",
        {"form": form, "instance": management_type, "object": management_type},
    )


@permission_required("calculator.delete_managementtype", raise_exception=True)
def managementtype_delete(request, pk):
    management_type = get_object_or_404(ManagementType, pk=pk)
    if request.method == "POST":
        if management_type.is_deletable:
            try:
                management_type.delete()
            except ProtectedError:
                messages.error(request, management_type.cant_delete_msg)
        else:
            messages.error(request, management_type.cant_delete_msg)

        if is_htmx(request):
            return htmx_response_trigger_close_modal(["resultsChanged"])
        return redirect("calculator:managementtype_list")

    return TemplateResponse(
        request,
        "frontpage/modal_confirm_delete.html",
        {"instance": management_type, "object": management_type},
    )
