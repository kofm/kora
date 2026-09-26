from django.contrib.auth.mixins import PermissionRequiredMixin
from django.http import HttpResponseBadRequest
from django.template.response import TemplateResponse
from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, UpdateView
from django_tables2 import RequestConfig

from breadcrumbs.utils import generate_breadcrumbs
from frontpage.utils.htmx import htmx_response_redirect, htmx_response_trigger_close_modal
from frontpage.views_decorators import NavPlantActiveContext, htmx_render_blocks, is_htmx, public_catalog_view
from register.filters import PlantSpeciesFilter
from register.models import PlantSpecies
from register.tables import PlantSpeciesTable


class PlantSpeciesCreate(PermissionRequiredMixin, NavPlantActiveContext, CreateView):
    model = PlantSpecies
    fields = ("common_name", "botanical_name", "code")
    template_name = "frontpage/modal_form.html"
    permission_required = ["register.add_plantspecies"]
    success_url = reverse_lazy("register:plantspecies_list")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["object_to_create"] = self.model._meta.verbose_name
        return context

    def form_valid(self, form):
        self.object = form.save()
        if is_htmx(self.request):
            return htmx_response_trigger_close_modal(["resultsChanged"])
        return htmx_response_redirect(self.success_url)


@public_catalog_view("register.view_plantspecies")
@htmx_render_blocks(["main"])
def plantspecies_list(request):
    flt = PlantSpeciesFilter(request.GET, PlantSpecies.objects.all())
    table = PlantSpeciesTable(flt.qs)
    RequestConfig(request, paginate={"per_page": 12}).configure(table)
    context = {"table": table, "filter": flt, **generate_breadcrumbs(request, PlantSpecies)}
    return TemplateResponse(request, "register/plantspecies_list.html", context)


class PlantSpeciesUpdateView(PermissionRequiredMixin, NavPlantActiveContext, UpdateView):
    model = PlantSpecies
    fields = ("common_name", "botanical_name", "code")
    template_name = "frontpage/modal_form.html"
    permission_required = ["register.change_plantspecies"]
    success_url = reverse_lazy("register:plantspecies_list")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["instance"] = self.object
        return context

    def form_valid(self, form):
        if is_htmx(self.request):
            self.object = form.save()
            return htmx_response_trigger_close_modal(["resultsChanged"])
        return super().form_valid(form)


class PlantSpeciesDeleteView(PermissionRequiredMixin, NavPlantActiveContext, DeleteView):
    object: PlantSpecies
    model = PlantSpecies
    success_url = reverse_lazy("register:plantspecies_list")
    permission_required = ["register.delete_plantspecies"]
    template_name = "frontpage/modal_confirm_delete.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["instance"] = self.object
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        if not self.object.is_deletable:
            return HttpResponseBadRequest("This species has varieties and cannot be deleted.")
        if is_htmx(request):
            self.object.delete()
            return htmx_response_trigger_close_modal(["resultsChanged"])
        return super().post(request, *args, **kwargs)
