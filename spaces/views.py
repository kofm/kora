from django.shortcuts import render
from django.views.generic import DetailView, ListView

from spaces.models import Location

class LocationList(ListView):
    model = Location

class LocationDetail(DetailView):
    model = Location
    context_object_name = "location"
