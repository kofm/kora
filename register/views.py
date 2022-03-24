from django.core.paginator import Paginator
from django.http.response import (
    HttpResponseRedirect,
)
from django.shortcuts import redirect, render
from django.urls.base import reverse, reverse_lazy
from django.views.generic import CreateView, DetailView, ListView
from django.views.generic.edit import DeleteView

from parameters.forms import SpeciesParameterForm, VarietalParameterForm

from .forms import PlantSpeciesForm, PlantVarietyForm, PlantVarietyNameForm
from .models import PlantSpecies, PlantVariety, PlantVarietyName

from django.db.models import CharField
from django.db.models.functions import Lower

CharField.register_lookup(Lower)


class PlantSpeciesList(ListView):
    model = PlantSpecies

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["nav_species"] = "active"
        return context


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
        varieties = self.get_related_varieties()
        context["varieties"] = varieties
        context["search"] = self.request.GET.get('search')
        return context

    def get_related_varieties(self):
        search = self.request.GET.get('search')
        if search and search != '':
            if len(search) < 2:
                queryset = self.object.variety.filter(names__name__istartswith=search)
            else:
                queryset = self.object.variety.filter(names__name__unaccent__lower__trigram_similar=search)
        else:
            queryset = self.object.variety.all()
        paginator = Paginator(queryset, 10)
        page = self.request.GET.get("page")
        varieties = paginator.get_page(page)
        return varieties


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
        queryset = self.object.speciesparameter_set.all()
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


class PlantVarietyDetail(DetailView):
    model = PlantVariety
    context_object_name = "variety"


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


def plantvariety_create(request, pk):
    species = PlantSpecies.objects.get(pk=pk)
    if request.POST:
        variety = PlantVarietyForm(request.POST)
        variety_name = PlantVarietyNameForm(request.POST)
        if variety.is_valid() and variety_name.is_valid():
            new_variety = variety.save()
            new_variety_name = variety_name.save(commit=False)
            new_variety_name.variety = new_variety
            new_variety_name.save()
            variety_name.save_m2m()
            return redirect(reverse_lazy('register:variety_detail', args=[new_variety.pk]))
    else:
        variety = PlantVarietyForm({"species": species})
        variety_name = PlantVarietyNameForm()
    return render(
        request,
        "register/plantvariety_form.html",
        {
            "plantvariety_form": variety,
            "plantvarietyname_form": variety_name,
            "species": species,
        },
    )

class PlantVarietyDelete(DeleteView):
    model = PlantVariety

    def get_success_url(self):
        return reverse_lazy('register:plantspecie_detail', args=[self.object.species.pk])

class PlantVarietyNameCreate(CreateView):
    model = PlantVarietyName
    fields = ['name', 'change_date', ]

    def get_success_url(self):
        return reverse_lazy('register:variety_detail', args=[self.kwargs['pk']])

    def form_valid(self, form):
        plantvariety = PlantVariety.objects.get(pk=self.kwargs['pk'])
        self.object = form.save(commit=False)
        self.object.variety = plantvariety
        self.object.save()
        return super().form_valid(form)

class PlantVarietyNameDelete(DeleteView):
    model = PlantVarietyName

    def get_success_url(self):
        return reverse_lazy('register:variety_detail', args=[self.object.variety.pk])
