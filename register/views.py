from functools import cached_property
from typing import Any, Dict, List, Tuple
from django.http import HttpRequest, HttpResponseBase

from django_tables2.config import RequestConfig

from collect.models import SeedSample
from collect.tables import SeedSampleTable
from django.core.paginator import Paginator
from django.db.models import CharField, Count
from django.db.models.functions import Lower
from django.http.response import HttpResponseRedirect, JsonResponse
from django.shortcuts import get_object_or_404, redirect
from django.template.response import TemplateResponse
from django.urls.base import reverse, reverse_lazy
from django.views.generic import CreateView, DetailView, ListView
from django.views.generic.edit import DeleteView, UpdateView
from frontpage.decorators import NavActive, nav_active
from parameters.forms import SpeciesParameterForm, VarietalParameterForm
from register.filters import EntityFilter, PlantVarietyFilter
from register.tables import (
    EntityTable,
    PlantVarietyEntityTable,
    PlantVarietyTable,
    ProtectionTable,
)
from view_breadcrumbs import BaseBreadcrumbMixin, CreateBreadcrumbMixin, DetailBreadcrumbMixin, ListBreadcrumbMixin, UpdateBreadcrumbMixin

from .forms import PlantSpeciesForm, PlantVarietyForm, ProtectionForm
from .models import Entity, PlantSpecies, PlantVariety, PlantVarietyName, Protection


CharField.register_lookup(Lower)


class NavActivePlants(NavActive):
    """A mixin for displaying the Plant menu item as selected."""
    def __init__(self) -> None:
        super().__init__("nav_plants")


# A decorator for displaying the Plant menu item as selected.
nav_active_plants = nav_active("nav_plants")


def custom_variety_crumbs(species: PlantSpecies, final_crumb: Tuple[str, str]) -> List[Tuple[str, str]]:
        """This function builds the custom breadcrumbs used in PlantVariety views.
        Home / Plants / Species / ...
        """
        return [
            (str(species._meta.verbose_name_plural.capitalize()), species.get_list_url()),
            (str(species), species.get_absolute_url()),
            final_crumb
        ]

class PlantSpeciesList(NavActivePlants, ListBreadcrumbMixin, ListView):
    model = PlantSpecies

    def get_queryset(self):
        queryset = (
            PlantSpecies.objects.all()
            .annotate(num_descriptions=Count("variety__description"))
            .order_by("-num_descriptions", "common_name")
        )
        return queryset


class PlantSpeciesCreate(NavActivePlants, CreateBreadcrumbMixin, CreateView):
    model = PlantSpecies
    form_class = PlantSpeciesForm
    template_name = "frontpage/_form.html"


    def get_context_data(self, **kwargs):
        context =  super().get_context_data(**kwargs)
        context["object_to_create"] = "Plant"
        return context


class PlantSpeciesUpdateView(NavActivePlants, UpdateBreadcrumbMixin, UpdateView):
    model = PlantSpecies
    fields = ["common_name", "latin_name", "plant_type"]


class PlantSpeciesDetailView(NavActivePlants, DetailBreadcrumbMixin, DetailView):
    model = PlantSpecies
    context_object_name = "species"
    template_name = "register/plantspecies_detail.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        filter = PlantVarietyFilter(
            self.request.GET, queryset=self.object.variety.all()
        )
        count = filter.qs.count()
        table = PlantVarietyTable(filter.qs)
        RequestConfig(self.request, paginate={"per_page": 25}).configure(table)
        context["table"] = table
        context["filter"] = filter
        context["count"] = count
        return context


class PlantSpeciesParametersList(NavActivePlants, DetailView):
    model = PlantSpecies
    context_object_name = "species"
    template_name = "register/plantspeciesparameters_list.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        parameters = self.get_related_parameters()
        context["nav_species"] = "active"
        context["parameters"] = parameters
        return context

    def get_related_parameters(self):
        queryset = self.object.parameters.all()
        paginator = Paginator(queryset, 5)
        page = self.request.GET.get("page")
        parameters = paginator.get_page(page)
        return parameters


class PlantVarietyParametersList(NavActivePlants, DetailView):
    model = PlantVariety
    context_object_name = "variety"
    template_name = "register/plantvarietyparameters_list.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["nav_species"] = "active"
        return context


class PlantVarietyUpdateView(NavActivePlants, UpdateView):
    model = PlantVariety
    fields = [
        "breeder",
    ]


class PlantVarietyDetail(NavActivePlants, BaseBreadcrumbMixin, DetailView):
    model = PlantVariety
    context_object_name = "variety"

    @cached_property
    def crumbs(self):
        return custom_variety_crumbs(self.object.species, (str(self.object), self.object.get_absolute_url()))

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context["seedsample_table"] = SeedSampleTable(
            SeedSample.objects.filter(variety=self.object.pk)
        )
        context["protection_table"] = ProtectionTable(
            Protection.objects.filter(variety=self.object.pk)
        )
        return context


@nav_active_plants
def add_speciesparametervervalue(request, pk):
    """
    https://stackoverflow.com/questions/37303171/django-create-new-object-in-form-update-select-box-and-save-it
    https://stackoverflow.com/questions/7782479/django-reverse-engineering-the-admin-sites-add-foreign-key-button
    Check this to add new parameter without leaving this view
    """
    species = PlantSpecies.objects.get(pk=pk)
    form = SpeciesParameterForm(initial={"specie": species})
    if request.method == "POST":
        form = SpeciesParameterForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(
                reverse(
                    "register:plantspeciesparameters_list", kwargs={"pk": species.id}
                )
            )

    context = {"form": form}
    return TemplateResponse(
        request, "register/plantspeciesparameters_create.html", context
    )


@nav_active_plants
def add_varietalparamevterervalue(request, pk):
    variety = PlantVariety.objects.get(pk=pk)
    form = VarietalParameterForm(initial={"variety": variety})
    if request.method == "POST":
        form = VarietalParameterForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect(
                reverse(
                    "register:plantvarietyparameters_list", kwargs={"pk": variety.id}
                )
            )

    context = {"form": form}
    return TemplateResponse(
        request, "register/plantspeciesparameters_create.html", context
    )


class PlantVarietyCreate(NavActivePlants, BaseBreadcrumbMixin, CreateView):
    model = PlantVariety
    form_class = PlantVarietyForm
    template_name = "frontpage/_form.html"

    def dispatch(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponseBase:
        """We retrieve the species we're operating within"""
        self.species = get_object_or_404(PlantSpecies, pk=self.kwargs["species_id"])
        return super().dispatch(request, *args, **kwargs)

    @cached_property
    def crumbs(self):
        return custom_variety_crumbs(self.species, ("Add Variety", ""))

    def get_initial(self):
        initial = super().get_initial()
        initial["species"] = self.species
        return initial

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context["species"] = self.species
        context["object_to_create"] = "Variety"
        return context


class PlantVarietyDelete(NavActivePlants, DeleteView):
    model = PlantVariety

    def get_success_url(self):
        return reverse_lazy(
            "register:plantspecies_detail", args=[self.object.species.pk]
        )


class PlantVarietyNameCreate(NavActivePlants, CreateView):
    model = PlantVarietyName
    fields = [
        "name",
        "change_date",
    ]

    def get_success_url(self):
        return reverse_lazy("register:plantvariety_detail", args=[self.kwargs["pk"]])

    def form_valid(self, form):
        plantvariety = PlantVariety.objects.get(pk=self.kwargs["pk"])
        self.object = form.save(commit=False)
        self.object.variety = plantvariety
        self.object.save()
        return super().form_valid(form)


class PlantVarietyNameUpdate(NavActivePlants, UpdateView):
    model = PlantVarietyName
    fields = [
        "name",
        "change_date",
    ]

    def get_success_url(self):
        return reverse_lazy(
            "register:plantvariety_detail", args=[self.object.variety.pk]
        )


class PlantVarietyNameDelete(NavActivePlants, DeleteView):
    model = PlantVarietyName

    def get_success_url(self):
        return reverse_lazy(
            "register:plantvariety_detail", args=[self.object.variety.pk]
        )


@nav_active_plants
def plantvariety_list(request, species_id):
    queryset = list(
        PlantVariety.objects.filter(species_id=species_id)
        .values("pk", "names__name")
        .distinct("pk")
        .order_by("pk", "-names__change_date")
    )
    return JsonResponse(queryset, safe=False)


@nav_active_plants
def protection_create(request, variety_id):
    variety = get_object_or_404(PlantVariety, pk=variety_id)
    if request.POST:
        form = ProtectionForm(request.POST)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.variety = variety
            instance.save()
            form.save_m2m()
            return redirect(instance.get_absolute_url())
    duplicate_id = request.GET.get("duplicate")
    if duplicate_id:
        try:
            protection_to_duplicate = Protection.objects.get(pk=duplicate_id)
            initial = {}
            initial["status"] = protection_to_duplicate.status
            initial["country"] = protection_to_duplicate.country
            initial["applicants"] = protection_to_duplicate.applicants.all()
            initial["maintainer"] = protection_to_duplicate.maintainer
            initial["date_start"] = protection_to_duplicate.date_start
            initial["date_end"] = protection_to_duplicate.date_end
            form = ProtectionForm(initial=initial)
        except Protection.DoesNotExist:
            pass
    else:
        form = ProtectionForm()
    return TemplateResponse(
        request,
        "register/protection_form.html",
        {
            "form": form,
            "variety": variety,
        },
    )


@nav_active_plants
def protection_update(request, pk):
    context = {}
    protection = get_object_or_404(Protection, pk=pk)
    if request.method == "POST":
        form = ProtectionForm(request.POST, instance=protection)
        if form.is_valid():
            instance = form.save()
            return redirect(instance.get_absolute_url())
    else:
        form = ProtectionForm(instance=protection)
        context["form"] = form
        context["protection"] = protection
        context["variety"] = protection.variety
    return TemplateResponse(request, "register/protection_form.html", context)


class ProtectionDeleteView(DeleteView):
    model = Protection

    def get_success_url(self):
        return reverse_lazy(
            "register:plantvariety_detail", args=[self.object.variety.pk]
        )


class ProtectionDetailView(NavActivePlants, DetailView):
    model = Protection


class EntityCreateView(NavActivePlants, CreateView):
    model = Entity
    fields = "__all__"


@nav_active_plants
def entity_detail(request, pk):
    context = {}
    entity = get_object_or_404(Entity, pk=pk)
    context["entity"] = entity
    context["varieties_table"] = PlantVarietyEntityTable(entity.plantvariety_set.all())
    return TemplateResponse(request, "register/entity_detail.html", context)


class EntityUpdateView(NavActivePlants, UpdateView):
    model = Entity
    fields = "__all__"


@nav_active_plants
def entity_list(request):
    context = {}
    filter = EntityFilter(request.GET, queryset=Entity.objects.all())
    table = EntityTable(filter.qs)
    RequestConfig(request, paginate={"per_page": 25}).configure(table)
    context["table"] = table
    context["filter"] = filter
    return TemplateResponse(request, "register/entity_list.html", context)
