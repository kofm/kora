from django.contrib.auth.mixins import PermissionRequiredMixin
from django.core.paginator import Paginator
from django.template.response import TemplateResponse
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic import CreateView, DeleteView, DetailView, UpdateView
from django_tables2 import RequestConfig

import breadcrumbs.generic as crumbs
from breadcrumbs.utils import generate_breadcrumbs
from frontpage.utils.htmx import htmx_response_redirect
from frontpage.views_decorators import NavPlantActiveContext, htmx_render_blocks, public_catalog_view
from register.filters import PlantSpeciesFilter
from register.models import PlantSpecies
from register.tables import PlantVarietyTable


class PlantSpeciesCreate(PermissionRequiredMixin, NavPlantActiveContext, CreateView):
    model = PlantSpecies
    fields = ("common_name", "latin_name", "plant_type")
    template_name = "frontpage/modal_form.html"
    permission_required = ["register.add_plantspecies"]

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["object_to_create"] = self.model._meta.verbose_name
        return context

    def form_valid(self, form):
        self.object = form.save()
        return htmx_response_redirect(self.object.get_absolute_url())


@public_catalog_view("register.view_plantspecies")
@htmx_render_blocks(["cards"])
def plantspecies_list(request):
    queryset = PlantSpecies.objects.all()
    flt = PlantSpeciesFilter(request.GET, queryset)
    paginator = Paginator(flt.qs, 12)
    page = request.GET.get("page", 1)
    page_obj = paginator.page(page)
    context = {"page_obj": page_obj, "filter": flt}
    context.update(generate_breadcrumbs(request, PlantSpecies))
    return TemplateResponse(request, "register/plantspecies_list.html", context)


@method_decorator(public_catalog_view("register.view_plantspecies"), name="dispatch")
class PlantSpeciesDetailView(crumbs.DetailBreadcrumbsMixin, NavPlantActiveContext, DetailView):
    model = PlantSpecies

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        queryset = self.object.variety.all()
        table = PlantVarietyTable(queryset)
        RequestConfig(self.request, paginate={"per_page": 15}).configure(table)
        context["table"] = table
        return context


class PlantSpeciesUpdateView(PermissionRequiredMixin, crumbs.UpdateBreadcrumbsMixin, NavPlantActiveContext, UpdateView):
    model = PlantSpecies
    fields = ("common_name", "latin_name", "plant_type")
    template_name = "frontpage/_update_form.html"
    permission_required = ["register.change_plantspecies"]


class PlantSpeciesDeleteView(PermissionRequiredMixin, NavPlantActiveContext, DeleteView):
    object: PlantSpecies
    model = PlantSpecies
    success_url = reverse_lazy("register:plantspecies_list")
    permission_required = ["register.delete_plantspecies"]
