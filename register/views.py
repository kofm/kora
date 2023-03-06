from typing import Any, Dict
from django.core.paginator import Paginator
from django.http.response import (
    HttpResponseRedirect,
    JsonResponse,
)
from django.shortcuts import get_object_or_404, redirect, render
from django.template.response import TemplateResponse
from django.urls.base import reverse, reverse_lazy
from django.views.generic import CreateView, DetailView, ListView
from django.views.generic.edit import DeleteView, UpdateView
from django_tables2.config import RequestConfig
from collect.models import SeedSample
from collect.tables import SeedSampleTable

from parameters.forms import SpeciesParameterForm, VarietalParameterForm
from register.tables import EntityTable, PlantVarietyEntityTable, ProtectionTable
from register.utils import paged_object_list_context

from .forms import PlantSpeciesForm, PlantVarietyForm, ProtectionForm
from .models import Entity, PlantSpecies, PlantVariety, PlantVarietyName, Protection

from django.db.models import CharField, Count
from django.db.models.functions import Lower

CharField.register_lookup(Lower)


class PlantSpeciesList(ListView):
    model = PlantSpecies

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["nav_species"] = "active"
        return context

    def get_queryset(self):
        queryset = (
            PlantSpecies.objects.all()
            .annotate(num_descriptions=Count("variety__description"))
            .order_by("-num_descriptions", "common_name")
        )
        return queryset


class PlantSpeciesCreate(CreateView):
    model = PlantSpecies
    form_class = PlantSpeciesForm
    context_object_name = "species"
    success_url = "/register/species/"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["nav_species"] = "active"
        return context


class PlantSpeciesDetail(DetailView):
    """This display the varieties present for the species and allow the
    user to create a new variety"""

    model = PlantSpecies
    template_name = "register/plantspecies_detail.html"
    context_object_name = "species"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["nav_species"] = "active"
        varieties, page_range = self.get_related_varieties()
        context["varieties"] = varieties
        context["page_range"] = page_range
        context["search"] = self.request.GET.get("search")
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


class PlantSpeciesParametersList(DetailView):
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


class PlantVarietyParametersList(DetailView):
    model = PlantVariety
    context_object_name = "variety"
    template_name = "register/plantvarietyparameters_list.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["nav_species"] = "active"
        return context


class PlantVarietyUpdateView(UpdateView):
    model = PlantVariety
    fields = [
        "breeder",
    ]


class PlantVarietyDetail(DetailView):
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
    return render(request, "register/plantspeciesparameters_create.html", context)


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
    return render(request, "register/plantspeciesparameters_create.html", context)


class PlantVarietyCreate(CreateView):
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

    def form_valid(self, form):
        response = super().form_valid(form)
        plantvariety_name = PlantVarietyName(name=self.object.name, variety=self.object)
        plantvariety_name.save()
        return response


class PlantVarietyDelete(DeleteView):
    model = PlantVariety

    def get_success_url(self):
        return reverse_lazy(
            "register:plantspecies-detail", args=[self.object.species.pk]
        )


class PlantVarietyNameCreate(CreateView):
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


class PlantVarietyNameUpdate(UpdateView):
    model = PlantVarietyName
    fields = [
        "name",
        "change_date",
    ]

    def get_success_url(self):
        return reverse_lazy(
            "register:plantvariety-detail", args=[self.object.variety.pk]
        )


class PlantVarietyNameDelete(DeleteView):
    model = PlantVarietyName

    def get_success_url(self):
        return reverse_lazy(
            "register:plantvariety-detail", args=[self.object.variety.pk]
        )


def plantvariety_list(request, species_id):
    queryset = list(
        PlantVariety.objects.filter(species_id=species_id)
        .values("pk", "names__name")
        .distinct("pk")
        .order_by("pk", "-names__change_date")
    )
    return JsonResponse(queryset, safe=False)


def protection_create(request, variety_id):
    variety = get_object_or_404(PlantVariety, pk=variety_id)
    if request.POST:
        form = ProtectionForm(request.POST)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.variety = variety
            instance.save()
            return redirect(instance.get_absolute_url())
    form = ProtectionForm()
    return TemplateResponse(
        request,
        "register/protection_form.html",
        {
            "form": form,
            "variety": variety,
        },
    )


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
    return TemplateResponse(request, "register/protection_form.html", context)


class ProtectionDetailView(DetailView):
    model = Protection


class EntityCreateView(CreateView):
    model = Entity
    fields = "__all__"


def entity_detail(request, pk):
    context = {}
    entity = get_object_or_404(Entity, pk=pk)
    context["entity"] = entity
    context["varieties_table"] = PlantVarietyEntityTable(entity.plantvariety_set.all())
    return TemplateResponse(request, "register/entity_detail.html", context)


class EntityUpdateView(UpdateView):
    model = Entity
    fields = "__all__"


def entity_list(request):
    context = {}
    # queryset = Entity.objects.all()
    # context["object_list"] = queryset
    table = EntityTable(Entity.objects.all())
    RequestConfig(request, paginate={"per_page": 25}).configure(table)
    context["table"] = table
    return TemplateResponse(request, "register/entity_list.html", context)
