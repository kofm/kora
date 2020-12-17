from django.shortcuts import render, reverse
from django.http import HttpResponse
from django.views.generic import ListView,DetailView,CreateView,View,FormView
from django.views.generic.detail import SingleObjectMixin
from .models import PlantSpecies,PlantVariety
from .forms import PlantSpeciesForm, PlantVarietyForm

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

class PlantSpeciesDetail(DetailView):
    model = PlantSpecies
    context_object_name = 'species'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = PlantVarietyForm()
        return context

    def post(self, request, *args, **kwargs):
        new_variety = PlantVariety(name = request.POST.get('name'),
                species=self.get_object())
        new_variety.save()
        return self.get(self, request, *args, **kwargs)

class PlantVarietyDetail(DetailView):
    model = PlantVariety
    context_object_name = 'variety'




def debug_request(request):
    return HttpResponse(request)
