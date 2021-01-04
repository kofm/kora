from describe.forms import TraitFormset
from django.shortcuts import get_object_or_404, redirect, render
from django.views.generic import ListView, DetailView
from .models import Description, Protocol
from register.models import PlantSpecies

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



def manage_trait(request, pk):
    """
    Edit trait and their states for a protocol.
    https://github.com/philgyford/django-nested-inline-formsets-example/
    """

    protocol = get_object_or_404(Protocol, id=pk)

    if request.method == 'POST':
        import pdb; pdb.set_trace()
        formset = TraitFormset(request.POST, instance=protocol)
        if formset.is_valid():
            formset.save()
            return redirect('describe:protocol_detail', pk=protocol.pk)
    else:
        formset = TraitFormset(instance=protocol)

    return render(request, 'describe/manage_trait.html', {
                  'protocol': protocol,
                  'trait_formset':formset}
                  )
