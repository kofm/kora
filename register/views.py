from django.shortcuts import reverse
from django.views.generic import CreateView, DetailView, ListView
from django.views.generic.edit import FormMixin

from .forms import PlantSpeciesForm, PlantVarietyForm
from .models import PlantSpecies, PlantVariety

class PlantSpeciesList(ListView):
    model = PlantSpecies

class PlantSpeciesCreate(CreateView):
    model = PlantSpecies
    form_class = PlantSpeciesForm
    context_object_name = 'species'
    success_url = "/register/species/"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["plantspecies_list"] = PlantSpecies.objects.all()
        return context

class PlantSpeciesDetail(FormMixin, DetailView):
    """This display the varieties present for the species and allow the
    user to create a new variety"""
    model = PlantSpecies
    form_class = PlantVarietyForm
    template_name = "register/plantspecies_detail.html"
    context_object_name = 'species'

    def get_initial(self):
        return {"species": self.get_object()}

    def get_success_url(self):
        return reverse("register:plantspecie_detail", kwargs={"pk": self.get_object().pk})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form"] = self.get_form()
        return context

    def post(self, request, **kwargs):
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        return self.form_invalid(form)

    def form_valid(self, form):
        plant_variety = PlantVariety(**form.cleaned_data)
        plant_variety.save()
        return super().form_valid(form)

class PlantVarietyDetail(DetailView):
    model = PlantVariety
    context_object_name = 'variety'
