from django.http.response import HttpResponse
from describe.forms import TraitForm, TraitFormSet
from django.views.generic import ListView, DetailView
from .models import Description, Protocol
from register.models import PlantSpecies
from django.shortcuts import get_object_or_404, render

class DescriptionsList(ListView):
    model = Description

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["nav_descriptions"] = "active"
        return context

class DescriptionDetail(DetailView):
    model = Description
    context_object_name = 'description'

class ProtocolsList(ListView):
    model = PlantSpecies
    template_name = 'describe/protocols_list.html'
    context_object_name = 'species'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["nav_protocols"] = "active"
        return context

class ProtocolDetail(DetailView):
    model = Protocol
    context_object_name = 'protocol'

def fset(request, pk):
    protocol = get_object_or_404(Protocol, pk = pk)
    if request.method == 'POST':
        form = TraitFormSet(request.POST, instance=protocol)
        #form = TraitForm(request.POST)
        if form.is_valid():
            return HttpResponse("Form valid")
    else:
        form = TraitFormSet(instance=protocol)
    return render(request, 'describe/fs.html', {'fs': form})
