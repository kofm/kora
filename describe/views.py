from django.http.response import HttpResponse, HttpResponseRedirect
from django.urls.base import reverse_lazy
from describe.forms import TraitForm, TraitFormSet
from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView, DeleteView
from .models import Description, Protocol
from register.models import PlantSpecies
from django.shortcuts import get_object_or_404, render
from django.urls import reverse

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

class ProtocolCreate(CreateView):
    model = Protocol
    fields = ['name', 'specie', 'url_ref',]
    template_name = 'describe/protocol_form.html'

    def get_success_url(self):
        return reverse('describe:protocol-update', args=(self.object.id,))

class ProtocolDelete(DeleteView):
    model = Protocol
    success_url = reverse_lazy('describe:protocols_list')

class ProtocolDetail(DetailView):
    model = Protocol
    context_object_name = 'protocol'

def fset(request, pk):
    protocol = get_object_or_404(Protocol, pk = pk)
    if request.method == 'POST':
        form = TraitFormSet(request.POST, instance=protocol)
        #form = TraitForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('describe:protocol_detail', kwargs={'pk': protocol.pk}))
    else:
        form = TraitFormSet(instance=protocol)
    return render(request, 'describe/fs.html', {'fs': form})
