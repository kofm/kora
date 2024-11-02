from django_tables2 import RequestConfig, SingleTableView

import breadcrumbs.generic as crumbs
from django.db.models import Count
from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, DetailView, UpdateView
from register.models import PlantSpecies, PlantVariety
from register.tables import PlantSpeciesTable, PlantVarietyTable
from register.views.base_views import NavActivePlants


class PlantSpeciesCreate(crumbs.CreateBreadcrumbsMixin, NavActivePlants, CreateView):
    model = PlantSpecies
    fields = ["common_name", "latin_name", "plant_type"]
    template_name = "frontpage/_create_form.html"

    def get_context_data(self, **kwargs):
        kwargs.update({"model_name": self.model._meta.verbose_name.title()})
        return super().get_context_data(**kwargs)


class PlantSpeciesList(crumbs.ListBreadcrumbsMixin, NavActivePlants, SingleTableView):
    model = PlantSpecies
    table_class = PlantSpeciesTable
    paginate_by = 10

    def get_queryset(self):
        queryset = PlantSpecies.objects.all().annotate(
            num_varieties=Count("variety"),
            num_accessions=Count("variety__seedsample"),
            num_parameters=Count("parameters"),
        )
        return queryset


class PlantSpeciesDetailView(crumbs.DetailBreadcrumbsMixin, NavActivePlants, DetailView):
    model = PlantSpecies

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        queryset = self.object.variety.all()
        table = PlantVarietyTable(queryset)
        RequestConfig(self.request, paginate={"per_page": 15}).configure(table)
        context["table"] = table
        return context


class PlantSpeciesUpdateView(crumbs.UpdateBreadcrumbsMixin, NavActivePlants, UpdateView):
    model = PlantSpecies
    fields = ["common_name", "latin_name", "plant_type"]
    template_name = "frontpage/_update_form.html"


class PlantSpeciesDeleteView(NavActivePlants, DeleteView):
    model = PlantSpecies
    success_url = reverse_lazy("register:plantspecies_list")
