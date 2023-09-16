from typing import Any, Dict

from django_tables2.config import RequestConfig

from collect.models import SeedSample
from collect.tables import SeedSampleTable
from django.core.paginator import Paginator
from django.db.models import CharField, Count, F, Window
from django.db.models.functions import Lag, Lead, Lower
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
from rest_framework import viewsets

from .forms import PlantSpeciesForm, PlantVarietyForm, ProtectionForm
from .models import Entity, PlantSpecies, PlantVariety, PlantVarietyName, Protection


CharField.register_lookup(Lower)


class NavActivePlants(NavActive):
    def __init__(self) -> None:
        super().__init__("nav_plants")


nav_active_plants = nav_active("nav_plants")


class PlantSpeciesList(NavActivePlants, ListView):
    model = PlantSpecies

    def get_queryset(self):
        queryset = (
            PlantSpecies.objects.all()
            .annotate(num_descriptions=Count("variety__description"))
            .order_by("-num_descriptions", "common_name")
        )
        return queryset


class PlantSpeciesCreate(NavActivePlants, CreateView):
    model = PlantSpecies
    form_class = PlantSpeciesForm
    context_object_name = "species"
    success_url = "/register/species/"


class PlantSpeciesUpdateView(NavActivePlants, UpdateView):
    model = PlantSpecies
    fields = ["common_name", "latin_name", "plant_type"]


class PlantSpeciesDetail(NavActivePlants, DetailView):
    """This display the varieties present for the species and allow the
    user to create a new variety"""

    model = PlantSpecies
    template_name = "register/plantspecies_detail.html"
    context_object_name = "species"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        varieties, page_range = self.get_related_varieties()
        context["varieties"] = varieties
        context["page_range"] = page_range
        context["search"] = self.request.GET.get("search")
        prev_next_records = PlantSpecies.objects.annotate(
            prev=Window(
                expression=Lag("pk", default=None), order_by=F("common_name").asc()
            ),
            next=Window(
                expression=Lead("pk", default=None), order_by=F("common_name").asc()
            ),
        ).values("pk", "prev", "next")
        prev_next_records_ids = list(
            filter(lambda x: x["pk"] == self.object.pk, prev_next_records)
        )[0]
        context.update(
            {
                "prev_record": prev_next_records_ids["prev"],
                "next_record": prev_next_records_ids["next"],
            }
        )
        return context

    def get_related_varieties(self):
        search = self.request.GET.get("search")
        if search and search != "":
            if len(search) < 3:
                queryset = self.object.variety.filter(names__name__istartswith=search)
            else:
                queryset = self.object.variety.filter(
                    names__name__unaccent__lower__trigram_similar=search
                )
        else:
            queryset = self.object.variety.all()
        paginator = Paginator(queryset, 10)
        page = self.request.GET.get("page")
        if not page:
            page = 1
        varieties = paginator.get_page(page)
        page_range = paginator.get_elided_page_range(number=page)
        return varieties, page_range


class PlantSpeciesDetailView(NavActivePlants, DetailView):
    model = PlantSpecies
    context_object_name = "species"
    template_name = "register/plantspecies_detailn.html"

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


class PlantVarietyDetail(NavActivePlants, DetailView):
    model = PlantVariety
    context_object_name = "variety"

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


class PlantVarietyCreate(NavActivePlants, CreateView):
    model = PlantVariety
    form_class = PlantVarietyForm

    def get_initial(self):
        initial = super().get_initial()
        initial = initial.copy()
        initial["species"] = self.kwargs["species_id"]
        return initial

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context["species"] = PlantSpecies.objects.get(pk=self.kwargs["species_id"])
        return context

    def get_success_url(self) -> str:
        return reverse_lazy("register:plantvariety-detail", args=[self.object.pk])


class PlantVarietyDelete(NavActivePlants, DeleteView):
    model = PlantVariety

    def get_success_url(self):
        return reverse_lazy(
            "register:plantspecies-detail", args=[self.object.species.pk]
        )


class PlantVarietyNameCreate(NavActivePlants, CreateView):
    model = PlantVarietyName
    fields = [
        "name",
        "change_date",
    ]

    def get_success_url(self):
        return reverse_lazy("register:plantvariety-detail", args=[self.kwargs["pk"]])

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
            "register:plantvariety-detail", args=[self.object.variety.pk]
        )


class PlantVarietyNameDelete(NavActivePlants, DeleteView):
    model = PlantVarietyName

    def get_success_url(self):
        return reverse_lazy(
            "register:plantvariety-detail", args=[self.object.variety.pk]
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
            "register:plantvariety-detail", args=[self.object.variety.pk]
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
