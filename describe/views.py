from django.shortcuts import render
from django.views.generic import ListView,DetailView
from .models import Description,Protocol
from register.models import PlantSpecies

class DescriptionsList(ListView):
    model = Description

class DescriptionDetail(DetailView):
    model = Description
    context_object_name = 'description'
    
class ProtocolsList(ListView):
    model = PlantSpecies
    template_name = 'describe/protocols_list.html'
    context_object_name = 'species'

class ProtocolDetail(DetailView):
    model = Protocol
    context_object_name = 'protocol'
