from django.urls.base import reverse_lazy
from django.views.generic import DetailView, ListView
from django.views.generic.edit import UpdateView
from parameters.models import Parameter

from spaces.models import Area, Location

class LocationListView(ListView):
    model = Location

class LocationDetailView(DetailView):
    model = Location
    context_object_name = "location"

class AreaDetailView(DetailView):
    model = Area
    context_object_name = 'area'

    def get_context_data(self, **kwargs):
        context =  super().get_context_data(**kwargs)
        context["parameters"] = Parameter.objects.all()
        return context

class AreaUpdateView(UpdateView):
    model = Area
    fields = ['name', 'width', 'length']
    def get_success_url(self):
        return reverse_lazy("spaces:area-detail", args=[self.object.id])
