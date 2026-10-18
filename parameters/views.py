from urllib.parse import urlsplit

from django.contrib.auth.decorators import permission_required
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.http import HttpResponseBadRequest
from django.shortcuts import get_object_or_404, redirect
from django.template.response import TemplateResponse
from django.urls import Resolver404, resolve, reverse_lazy
from django.urls.base import reverse
from django.views.generic import CreateView, DeleteView, UpdateView
from django_tables2 import RequestConfig

from breadcrumbs.utils import generate_breadcrumbs
from frontpage.autocomplete import AutocompleteModelView
from frontpage.headers import ListHeader
from frontpage.utils.htmx import htmx_response_redirect, htmx_response_trigger_close_modal
from frontpage.utils.shortcuts import get_safe_next_url
from frontpage.views_decorators import htmx_render_partial, is_htmx, nav_active
from parameters.filters import ParameterFilter, VarietalParameterFilter
from parameters.forms import (
    ParameterForm,
    VarietalParameterForm,
    VarietalParameterUpdateForm,
    VarietyVarietalParameterForm,
)
from parameters.tables import (
    ParameterTable,
    VarietalParameterTable,
)
from register.models import PlantVariety

from .models import Parameter, VarietalParameter


@nav_active("nav_plan")
@htmx_render_partial("main", template_name="frontpage/list.html")
def parameter_list(request):
    queryset = Parameter.objects.all()
    flt = ParameterFilter(request.GET, queryset=queryset)
    table = ParameterTable(flt.qs)
    RequestConfig(request).configure(table)
    context = {
        "page_obj": queryset,
        "table": table,
        "filter": flt,
        "header": ListHeader(request, Parameter, modal=True),
        **generate_breadcrumbs(request, Parameter),
    }
    return TemplateResponse(request, "parameters/parameter_list.html", context)


class ParameterCreate(PermissionRequiredMixin, CreateView):
    model = Parameter
    form_class = ParameterForm
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
    form_class = ParameterForm
    template_name = "frontpage/modal_form.html"
    success_url = reverse_lazy("parameters:parameter_list")
    permission_required = ["parameters.change_parameter"]

    def get_context_data(self, **kwargs):
        return super().get_context_data(instance=self.object, **kwargs)

    def form_valid(self, form):
        self.object = form.save()
        if is_htmx(self.request):
            return htmx_response_trigger_close_modal(["resultsChanged"])
        return super().form_valid(form)


class ParameterDelete(PermissionRequiredMixin, DeleteView):
    model = Parameter
    success_url = reverse_lazy("parameters:parameter_list")
    permission_required = ["parameters.delete_parameter"]

    def get_template_names(self):
        if is_htmx(self.request):
            return ["frontpage/modal_confirm_delete.html"]
        return super().get_template_names()

    def get_context_data(self, **kwargs):
        return super().get_context_data(instance=self.object, **kwargs)

    def form_valid(self, form):
        response = super().form_valid(form)
        if is_htmx(self.request):
            return htmx_response_trigger_close_modal(["resultsChanged"])
        return response

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        if not self.object.is_deletable:
            return HttpResponseBadRequest("This parameter has observations and cannot be deleted.")
        return super().post(request, *args, **kwargs)


@htmx_render_partial("main", template_name="frontpage/list.html")
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
        "header": ListHeader(request, VarietalParameter, modal=True),
        **generate_breadcrumbs(request, VarietalParameter),
    }
    return TemplateResponse(request, "parameters/varietalparameter_list.html", context)


@permission_required("parameters.add_varietalparameter", raise_exception=True)
def varietalparameter_create(request):
    if request.method == "POST":
        form = VarietalParameterForm(request.POST, parameter_refresh_url=request.get_full_path())
        if form.is_valid():
            form.save()
            success_url = reverse("parameters:varietalparameter_list")
            if is_htmx(request):
                return htmx_response_redirect(success_url)
            return redirect(success_url)
    else:
        form = VarietalParameterForm(initial=request.GET.dict(), parameter_refresh_url=request.get_full_path())

    return TemplateResponse(
        request,
        "frontpage/modal_form.html",
        {"form": form, "object_to_create": "Value"},
    )


@permission_required("parameters.add_varietalparameter", raise_exception=True)
def variety_varietalparameter_create(request, variety_pk):
    variety = get_object_or_404(PlantVariety, pk=variety_pk)

    if request.method == "POST":
        form = VarietyVarietalParameterForm(request.POST, parameter_refresh_url=request.get_full_path())
        if form.is_valid():
            instance = form.save(commit=False)
            instance.variety = variety
            instance.save()
            success_url = reverse("register:variety_detail", args=[variety.pk])
            if is_htmx(request):
                return htmx_response_redirect(success_url)
            return redirect(success_url)
    else:
        form = VarietyVarietalParameterForm(initial=request.GET.dict(), parameter_refresh_url=request.get_full_path())

    return TemplateResponse(
        request,
        "frontpage/modal_form.html",
        {"form": form, "object_to_create": f"Value for {variety.name}"},
    )


def _varietalparameter_success_response(request):
    success_url = get_safe_next_url(request, reverse("parameters:varietalparameter_list"))
    if not is_htmx(request):
        return redirect(success_url)

    try:
        origin = resolve(urlsplit(success_url).path).view_name
    except Resolver404:
        origin = None
    if origin == "parameters:varietalparameter_list":
        return htmx_response_trigger_close_modal(["resultsChanged"])
    return htmx_response_redirect(success_url)


@permission_required("parameters.change_varietalparameter", raise_exception=True)
def varietalparameter_update(request, pk):
    value = get_object_or_404(VarietalParameter, pk=pk)
    form = VarietalParameterUpdateForm(instance=value)
    if request.method == "POST":
        form = VarietalParameterUpdateForm(request.POST, instance=value)
        if form.is_valid():
            form.save()
            return _varietalparameter_success_response(request)
    template = "frontpage/modal_form.html" if is_htmx(request) else "parameters/varietalparameter_update.html"
    return TemplateResponse(request, template, {"form": form, "instance": value})


@permission_required("parameters.delete_varietalparameter", raise_exception=True)
def varietalparameter_delete(request, pk):
    param = get_object_or_404(VarietalParameter, pk=pk)
    if request.method == "POST":
        param.delete()
        return _varietalparameter_success_response(request)
    template = (
        "parameters/partials/varietalparameter_modal_confirm_delete.html"
        if is_htmx(request)
        else "parameters/varietalparameter_confirm_delete.html"
    )
    return TemplateResponse(request, template, {"param": param, "instance": param})


class ParameterAutocompleteView(AutocompleteModelView):
    model = Parameter
    search_fields = ["code", "name"]
    value_fields = ["id", "code", "name"]
    ordering = ["code", "name", "pk"]
