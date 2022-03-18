from django.core import serializers
from django.core.paginator import Paginator
from django.http.response import Http404, HttpResponse, HttpResponseBadRequest, HttpResponseRedirect, JsonResponse
from django.shortcuts import redirect, render, reverse
from django.views.generic import CreateView, DetailView, ListView
from django.views.generic.edit import FormMixin, UpdateView

from parameters.forms import SpeciesParameterForm, VarietalParameterForm
from parameters.models import SpeciesParameter

from .forms import PlantSpeciesForm, PlantVarietyForm
from .models import PlantSpecies, PlantVariety

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

class PlantSpeciesDetail(FormMixin, DetailView):
    """This display the varieties present for the species and allow the
    user to create a new variety"""

    model = PlantSpecies
    form_class = PlantVarietyForm
    template_name = "register/plantspecies_detail.html"
    context_object_name = "species"

    def get_initial(self):
        return {"species": self.get_object()}

    def get_success_url(self):
        return reverse(
            "register:plantspecie_detail", kwargs={"pk": self.get_object().pk}
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["nav_species"] = "active"
        context["form"] = self.get_form()
        varieties = self.get_related_varieties()
        context["varieties"] = varieties
        return context

    def post(self, request, **kwargs):
        self.object = self.get_object()
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_valid(self, form):
        plant_variety = PlantVariety(**form.cleaned_data)
        plant_variety.save()
        return super().form_valid(form)

    def get_related_varieties(self):
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
