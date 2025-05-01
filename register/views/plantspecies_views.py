from django.contrib.auth.mixins import PermissionRequiredMixin
from django.db.models import Count
from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, DetailView, UpdateView
from django_tables2 import RequestConfig, SingleTableView

import breadcrumbs.generic as crumbs
from frontpage.views_decorators import NavPlantActiveContext
from register.models import PlantSpecies
from register.tables import PlantSpeciesTable, PlantVarietyTable


class PlantSpeciesCreate(PermissionRequiredMixin, crumbs.CreateBreadcrumbsMixin, NavPlantActiveContext, CreateView):
    model = PlantSpecies
    fields = ("common_name", "latin_name", "plant_type")
    template_name = "frontpage/_create_form.html"
    permission_required = ["register.add_plantspecies"]


class PlantSpeciesList(crumbs.ListBreadcrumbsMixin, NavPlantActiveContext, SingleTableView):
    model = PlantSpecies
    table_class = PlantSpeciesTable
    paginate_by = 10

    def get_queryset(self):
        return PlantSpecies.objects.all().annotate(
            num_varieties=Count("variety", distinct=True),
            num_accessions=Count("variety__sample", distinct=True),
            num_parameters=Count("parameters", distinct=True),
        )


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
