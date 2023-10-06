from functools import cached_property
from typing import Any, Dict
from django.http import HttpRequest, HttpResponseBase
from django.shortcuts import get_object_or_404


from collect.models import SeedSample
from collect.tables import SeedSampleTable
from django.urls.base import reverse_lazy
from django.views.generic import DetailView
from django.views.generic.edit import DeleteView, UpdateView
from register.tables import ProtectionTable
from view_breadcrumbs import BaseBreadcrumbMixin

from register.forms import PlantVarietyForm
from register.models import PlantSpecies, PlantVariety, PlantVarietyName, Protection
from register.views.base_views import (
    NavActivePlants,
    custom_variety_crumbs,
)
from register.views.plantspecies_views import PlantCreateMixin


class PlantVarietyCreate(BaseBreadcrumbMixin, PlantCreateMixin):
    model = PlantVariety
    form_class = PlantVarietyForm

    def dispatch(
        self, request: HttpRequest, *args: Any, **kwargs: Any
    ) -> HttpResponseBase:
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
        return context


class PlantVarietyDetail(NavActivePlants, BaseBreadcrumbMixin, DetailView):
    model = PlantVariety
    context_object_name = "variety"

    @cached_property
    def crumbs(self):
        return custom_variety_crumbs(
            self.object.species, (str(self.object), self.object.get_absolute_url())
        )

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context["seedsample_table"] = SeedSampleTable(
            SeedSample.objects.filter(variety=self.object.pk)
        )
        context["protection_table"] = ProtectionTable(
            Protection.objects.filter(variety=self.object.pk)
        )
        return context


class PlantVarietyUpdateView(NavActivePlants, BaseBreadcrumbMixin, UpdateView):
    model = PlantVariety
    fields = [
        "breeder",
    ]

    @cached_property
    def crumbs(self):
        return custom_variety_crumbs(
            self.object.species,
            (self.object, self.object.get_absolute_url()),
            (f"Update: {self.object}", self.object.get_absolute_url()),
        )


class PlantVarietyDelete(NavActivePlants, DeleteView):
    model = PlantVariety

    def get_success_url(self):
        return reverse_lazy(
            "register:plantspecies_detail", args=[self.object.species.pk]
        )


class PlantVarietyNameCreate(BaseBreadcrumbMixin, PlantCreateMixin):
    model = PlantVarietyName
    fields = [
        "name",
        "change_date",
    ]

    @cached_property
    def crumbs(self):
        return custom_variety_crumbs(
            self.variety.species,
            (str(self.variety), self.variety.get_absolute_url()),
            (f"Add {self.model._meta.verbose_name.capitalize()}", ""),
        )

    def dispatch(
        self, request: HttpRequest, *args: Any, **kwargs: Any
    ) -> HttpResponseBase:
        self.variety = get_object_or_404(PlantVariety, pk=self.kwargs["pk"])
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["variety"] = self.variety
        return context

    def get_success_url(self):
        return reverse_lazy("register:plantvariety_detail", args=[self.kwargs["pk"]])

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.variety = self.variety
        self.object.save()
        return super().form_valid(form)


class PlantVarietyNameUpdate(NavActivePlants, BaseBreadcrumbMixin, UpdateView):
    model = PlantVarietyName
    fields = [
        "name",
        "change_date",
    ]

    @cached_property
    def crumbs(self):
        return custom_variety_crumbs(
            self.object.variety.species,
            (str(self.object.variety), self.object.variety.get_absolute_url()),
            (f"Update {self.model._meta.verbose_name.capitalize()}", ""),
        )

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
