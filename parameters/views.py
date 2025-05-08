from django import forms
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404, redirect
from django.template.response import TemplateResponse
from django.urls import reverse_lazy
from django.urls.base import reverse
from django.views.generic import CreateView, DeleteView, UpdateView
from django.views.generic.detail import DetailView
from django_tables2 import RequestConfig

from breadcrumbs.utils import generate_breadcrumbs
from frontpage.views_decorators import htmx_render_block_from_params, htmx_render_blocks, nav_active
from parameters.filters import ParameterFilter
from parameters.forms import VarietalParameterForm
from parameters.tables import (
    ParameterTable,
    SpeciesParameterTable,
    VarietalParameterTable,
)

from .models import Parameter, SpeciesParameter, VarietalParameter


@nav_active("nav_plan")
@htmx_render_blocks(["table"])
def parameter_list(request):
    queryset = Parameter.objects.all()
    flt = ParameterFilter(request.GET, queryset=queryset)
    table = ParameterTable(flt.qs)
    RequestConfig(request).configure(table)
    context = {"page_obj": queryset, "table": table, "filter": flt, **generate_breadcrumbs(request, Parameter)}
    return TemplateResponse(request, "parameters/parameter_list.html", context)


class ParameterCreate(PermissionRequiredMixin, CreateView):
    model = Parameter
    success_url = reverse_lazy("parameters:parameter_list")
    fields = "__all__"
    permission_required = ["parameters.add_parameter"]

    def get_form(self):
        form = super(ParameterCreate, self).get_form()
        form.fields["description"].widget = forms.Textarea()
        return form

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["nav_parameters"] = "active"
        return context


class ParameterUpdate(PermissionRequiredMixin, UpdateView):
    model = Parameter
    fields = "__all__"
    template_name = "parameters/parameter_form.html"
    success_url = reverse_lazy("parameters:parameter_list")
    permission_required = ["parameters.change_parameter"]

    def get_form(self):
        form = super(ParameterUpdate, self).get_form()
        form.fields["description"].widget = forms.Textarea()
        return form

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["nav_parameters"] = "active"
        return context


class ParameterDelete(PermissionRequiredMixin, DeleteView):
    model = Parameter
    success_url = reverse_lazy("parameters:parameter_list")
    permission_required = ["parameters.delete_parameter"]


class ParameterDetail(DetailView):
    model = Parameter
    context_object_name = "parameter"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["nav_parameters"] = "active"

        # The tables to display
        table_data = {
            "species_parameters_table": {"table": SpeciesParameterTable, "model": SpeciesParameter},
            "varietal_parameters_table": {"table": VarietalParameterTable, "model": VarietalParameter},
        }

        # Display the tables
        for key, value in table_data.items():
            table = value["table"](value["model"].objects.filter(parameter=self.object.pk))
            RequestConfig(self.request).configure(table)
            context[key] = table

        return context

    def get_related_cropparams(self):
        queryset = self.object.speciesparameter_set.all()
        paginator = Paginator(queryset, 5)
        page = self.request.GET.get("pagecp")
        cropparams = paginator.get_page(page)
        return cropparams

    def get_related_varparams(self):
        queryset = self.object.varietalparameter_set.all()
        paginator = Paginator(queryset, 5)
        page = self.request.GET.get("pagevp")
        varparams = paginator.get_page(page)
        return varparams


@nav_active("nav_plan")
@htmx_render_block_from_params()
def parameter_detail(request, pk):
    parameter = get_object_or_404(Parameter, pk=pk)
    vp_queryset = VarietalParameter.objects.select_related("variety__species", "parameter").filter(parameter=parameter)
    sp_queryset = SpeciesParameter.objects.select_related("specie", "parameter").filter(parameter=parameter)
    vptable = VarietalParameterTable(vp_queryset)
    sptable = SpeciesParameterTable(sp_queryset)
    rq = RequestConfig(request)
    rq.configure(vptable)
    rq.configure(sptable)
    context = {
        "parameter": parameter,
        "vp_table": vptable,
        "sp_table": sptable,
        **generate_breadcrumbs(request, Parameter, parameter),
    }
    return TemplateResponse(request, "parameters/parameter_detail.html", context)


class SpeciesParameterUpdate(UpdateView):
    model = SpeciesParameter
    fields = [
        "value",
        "url_ref",
    ]
    template_name = "parameters/cropparam_update.html"

    def get_success_url(self):
        return reverse("register:plantspecies_detail", kwargs={"pk": self.get_object().specie.pk})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["nav_species"] = "active"
        return context


def varietalparameter_update(request, pk):
    param = get_object_or_404(VarietalParameter, pk=pk)
    form = VarietalParameterForm(instance=param)
    if request.POST:
        form = VarietalParameterForm(request.POST, instance=param)
        if form.is_valid():
            form.save()
            return redirect(
                reverse_lazy(
                    "register:variety_detail",
                    args=[
                        param.variety.pk,
                    ],
                )
            )
    return TemplateResponse(request, "register/plantspeciesparameters_create.html", {"form": form})


def varietalparameter_delete(request, pk):
    param = get_object_or_404(VarietalParameter, pk=pk)
    if request.POST:
        param.delete()
        return redirect(
            reverse_lazy(
                "register:variety_detail",
                args=[
                    param.variety.pk,
                ],
            )
        )
    return TemplateResponse(request, "parameters/varietalparameter_confirm_delete.html", {"param": param})
