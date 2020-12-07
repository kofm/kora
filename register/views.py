from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic import ListView,DetailView
from .models import PlantSpecies,PlantVariety

def index(request):
   return HttpResponse("Hello world") 

class PlantSpeciesList(ListView):
    model = PlantSpecies

class PlantSpeciesDetail(DetailView):
    model = PlantSpecies
    context_object_name = 'species'

class PlantVarietyDetail(DetailView):
    model = PlantVariety
    context_object_name = 'variety'
