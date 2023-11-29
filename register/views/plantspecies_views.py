from django.db.models import Count
from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, DetailView, ListView, UpdateView
from django_tables2 import RequestConfig, SingleTableMixin, SingleTableView

from view_breadcrumbs import (
    CreateBreadcrumbMixin,
    DeleteBreadcrumbMixin,
    DetailBreadcrumbMixin,
    ListBreadcrumbMixin,
    UpdateBreadcrumbMixin,
)

from register.views.base_views import NavActivePlants, PlantCreateMixin
from register.models import PlantSpecies
from register.filters import PlantVarietyFilter
from register.tables import PlantSpeciesTable, PlantVarietyTable


class PlantSpeciesCreate(CreateBreadcrumbMixin, PlantCreateMixin):
    model = PlantSpecies
    fields = ["common_name", "latin_name", "plant_type"]


class PlantSpeciesList(NavActivePlants, ListBreadcrumbMixin, SingleTableView):
    model = PlantSpecies
    table_class = PlantSpeciesTable
    paginate_by = 10

    def get_queryset(self):
        queryset = PlantSpecies.objects.all().annotate(
            num_varieties=Count("variety"), num_accessions=Count("variety__seedsample"), num_parameters=Count("parameters")
        )
        return queryset


class PlantSpeciesDetailView(NavActivePlants, DetailBreadcrumbMixin, DetailView):
    model = PlantSpecies
    context_object_name = "species"
    template_name = "register/plantspecies_detail.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        filter = PlantVarietyFilter(
            self.request.GET, queryset=self.object.variety.all().order_by("-created_at")
        )
        count = filter.qs.count()
        table = PlantVarietyTable(filter.qs)
        RequestConfig(self.request, paginate={"per_page": 25}).configure(table)
        context["table"] = table
        context["filter"] = filter
        context["count"] = count
        return context


class PlantSpeciesUpdateView(NavActivePlants, UpdateBreadcrumbMixin, UpdateView):
    model = PlantSpecies
    fields = ["common_name", "latin_name", "plant_type"]


class PlantSpeciesDeleteView(NavActivePlants, DeleteBreadcrumbMixin, DeleteView):
    model = PlantSpecies
    success_url = reverse_lazy("register:plantspecies_list")
