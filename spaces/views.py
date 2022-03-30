from django.urls.base import reverse_lazy
from django.views.generic import DetailView, ListView
from django.views.generic.edit import UpdateView
from calculator.models import Crop
from parameters.models import Parameter
import pandas as pd

from spaces.models import Area, Location

class LocationListView(ListView):
    model = Location

    def get_context_data(self, **kwargs):
        context =  super().get_context_data(**kwargs)
        context["crop_totals"] = self.get_crop_totals()
        return context

    def get_crop_totals(self):
        a=[]
        for c in Crop.objects.all():
            a.append({'y': c.area.total_area, 'x': str(c.content_object)})
        d=pd.DataFrame(a).groupby('x', as_index=False).mean().sort_values(by='y', ascending=False)
        return d.to_dict(orient='records')

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
    fields = ['location', 'name', 'width', 'length']
    def get_success_url(self):
        return reverse_lazy("spaces:area-detail", args=[self.object.id])
