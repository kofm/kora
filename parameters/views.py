from django import forms
from django.core.paginator import Paginator
from django.shortcuts import render
from django.urls import reverse_lazy
from django.urls.base import reverse
from django.views.generic import CreateView, DeleteView, ListView, UpdateView
from django.views.generic.detail import DetailView
from django_tables2 import RequestConfig

from parameters.tables import ParameterTable, SpeciesParameterTable, VarietalParameterTable

from .models import SpeciesParameter, Parameter, VarietalParameter

class ParametersList(ListView):
    model = Parameter
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        parameters_table = ParameterTable(Parameter.objects.all())
        RequestConfig(self.request, paginate={"per_page": 10}).configure(parameters_table)
        context["parameters_table"] = parameters_table
        context["nav_parameters"] = "active"
        return context


class ParameterCreate(CreateView):
    model = Parameter
    success_url = reverse_lazy("parameters:parameters-list")
    fields = "__all__"

    def get_form(self):
        form = super(ParameterCreate, self).get_form()
        form.fields["description"].widget = forms.Textarea()
        return form

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["nav_parameters"] = "active"
        return context

class ParameterUpdate(UpdateView):
    model = Parameter
    fields = "__all__"
    template_name = "parameters/parameter_form.html"
    success_url = reverse_lazy("parameters:parameters-list")

    def get_form(self):
        form = super(ParameterUpdate, self).get_form()
        form.fields["description"].widget = forms.Textarea()
        return form

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["nav_parameters"] = "active"
        return context

class ParameterDelete(DeleteView):
    model = Parameter
    success_url = reverse_lazy("parameters:parameters-list")

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
            table = value["table"](
                value["model"].objects.filter(parameter=self.object.pk)
            )
            RequestConfig(self.request, paginate={"per_page": 10}).configure(table)
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

class SpeciesParameterUpdate(UpdateView):
    model = SpeciesParameter
    fields = [
        "value",
        "url_ref",
    ]
    template_name = "parameters/cropparam_update.html"

    def get_success_url(self):
        return reverse(
            "register:plantspecies_detail", kwargs={"pk": self.get_object().specie.pk}
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["nav_species"] = "active"
        return context
