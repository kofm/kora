from django.contrib.auth.decorators import permission_required
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.http import HttpResponseBadRequest
from django.shortcuts import get_object_or_404, redirect
from django.template.response import TemplateResponse
from django.urls import reverse_lazy
from django.urls.base import reverse
from django.views.generic import CreateView, DeleteView, UpdateView
from django_tables2 import RequestConfig

from breadcrumbs.utils import generate_breadcrumbs
from frontpage.autocomplete import AutocompleteModelView
from frontpage.utils.htmx import htmx_response_redirect, htmx_response_trigger_close_modal
from frontpage.utils.shortcuts import get_safe_next_url
from frontpage.views_decorators import htmx_render_block_from_params, htmx_render_blocks, is_htmx, nav_active
from parameters.filters import ParameterFilter, VarietalParameterFilter
from parameters.forms import VarietalParameterForm, VarietyVarietalParameterForm
from parameters.tables import (
    ParameterTable,
    VarietalParameterTable,
)
from register.models import PlantVariety

from .models import Parameter, VarietalParameter


@nav_active("nav_plan")
@htmx_render_blocks(["main"])
def parameter_list(request):
    queryset = Parameter.objects.all()
    flt = ParameterFilter(request.GET, queryset=queryset)
    table = ParameterTable(flt.qs)
    RequestConfig(request).configure(table)
    context = {"page_obj": queryset, "table": table, "filter": flt, **generate_breadcrumbs(request, Parameter)}
    return TemplateResponse(request, "parameters/parameter_list.html", context)


class ParameterCreate(PermissionRequiredMixin, CreateView):
    model = Parameter
    fields = "__all__"
    success_url = reverse_lazy("parameters:parameter_list")
    template_name = "frontpage/modal_form.html"
    permission_required = ["parameters.add_parameter"]

    def form_valid(self, form):
        self.object = form.save()
        if is_htmx(self.request):
            return htmx_response_trigger_close_modal(["resultsChanged"])
        return super().form_valid(form)


class ParameterUpdate(PermissionRequiredMixin, UpdateView):
    model = Parameter
    fields = "__all__"
    template_name = "frontpage/modal_form.html"
    success_url = reverse_lazy("parameters:parameter_list")
    permission_required = ["parameters.change_parameter"]

    def form_valid(self, form):
        self.object = form.save()
        if is_htmx(self.request):
            return htmx_response_redirect(reverse("parameters:parameter_detail", args=[self.object.pk]))
        return super().form_valid(form)


class ParameterDelete(PermissionRequiredMixin, DeleteView):
    model = Parameter
    success_url = reverse_lazy("parameters:parameter_list")
    permission_required = ["parameters.delete_parameter"]

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        if not self.object.is_deletable:
            return HttpResponseBadRequest("This parameter has observations and cannot be deleted.")
        return super().post(request, *args, **kwargs)


@nav_active("nav_describe")
@htmx_render_block_from_params()
def parameter_detail(request, pk):
    parameter = get_object_or_404(Parameter, pk=pk)
    queryset = VarietalParameter.objects.select_related("variety__species", "parameter").filter(parameter=parameter)
    table = VarietalParameterTable(queryset)
    rq = RequestConfig(request)
    rq.configure(table)
    context = {
        "parameter": parameter,
        "table": table,
        **generate_breadcrumbs(request, Parameter, parameter),
    }
    return TemplateResponse(request, "parameters/parameter_detail.html", context)


@htmx_render_blocks(["main"])
@permission_required("parameters.view_varietalparameter", raise_exception=True)
def varietalparameter_list(request):
    flt = VarietalParameterFilter(
        request.GET, queryset=VarietalParameter.objects.select_related("variety__species", "parameter").all()
    )
    table = VarietalParameterTable(flt.qs)
    RequestConfig(request, paginate={"per_page": 10}).configure(table)
    context = {
        "table": table,
        "filter": flt,
        **generate_breadcrumbs(request, VarietalParameter),
    }
    return TemplateResponse(request, "parameters/varietalparameter_list.html", context)


@permission_required("parameters.add_varietalparameter", raise_exception=True)
def varietalparameter_create(request):
    if request.method == "POST":
        form = VarietalParameterForm(request.POST)
        if form.is_valid():
            form.save()
            success_url = reverse("parameters:varietalparameter_list")
            if is_htmx(request):
                return htmx_response_redirect(success_url)
            return redirect(success_url)
    else:
        form = VarietalParameterForm()

    return TemplateResponse(
        request,
        "frontpage/modal_form.html",
        {"form": form, "object_to_create": "Value"},
    )


@permission_required("parameters.add_varietalparameter", raise_exception=True)
def variety_varietalparameter_create(request, variety_pk):
    variety = get_object_or_404(PlantVariety, pk=variety_pk)

    if request.method == "POST":
        form = VarietyVarietalParameterForm(request.POST)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.variety = variety
            instance.save()
            success_url = reverse("register:variety_detail", args=[variety.pk])
            if is_htmx(request):
                return htmx_response_redirect(success_url)
            return redirect(success_url)
    else:
        form = VarietyVarietalParameterForm()

    return TemplateResponse(
        request,
        "frontpage/modal_form.html",
        {"form": form, "object_to_create": f"Value for {variety.name}"},
    )


@permission_required("parameters.change_varietalparameter", raise_exception=True)
def varietalparameter_update(request, pk):
    value = get_object_or_404(VarietalParameter, pk=pk)
    form = VarietyVarietalParameterForm(instance=value)
    if request.method == "POST":
        form = VarietyVarietalParameterForm(request.POST, instance=value)
        if form.is_valid():
            form.save()
            success_url = get_safe_next_url(request, reverse("parameters:varietalparameter_list"))
            return redirect(success_url)
    return TemplateResponse(request, "parameters/varietalparameter_update.html", {"form": form})


@permission_required("parameters.delete_varietalparameter", raise_exception=True)
def varietalparameter_delete(request, pk):
    param = get_object_or_404(VarietalParameter, pk=pk)
    if request.method == "POST":
        param.delete()
        success_url = get_safe_next_url(request, reverse("parameters:varietalparameter_list"))
        return redirect(success_url)
    return TemplateResponse(request, "parameters/varietalparameter_confirm_delete.html", {"param": param})


class ParameterAutocompleteView(AutocompleteModelView):
    model = Parameter
    search_fields = ["code", "name"]
    value_fields = ["id", "code", "name"]
    ordering = ["code", "name", "pk"]

    def get_label(self, obj):
        return f"{obj.name} ({obj.measure_unit})"
