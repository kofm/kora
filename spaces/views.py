from django.http.response import HttpResponse
from django.shortcuts import render
from django.urls.base import reverse_lazy
from django.views.decorators.http import require_http_methods
from django.views.generic import DetailView, ListView
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from calculator.models import Crop
from parameters.models import Parameter
import pandas as pd

from spaces.models import Area, Location


class LocationListView(ListView):
    model = Location

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["crop_total_areas"] = self.get_crop_total_areas()
        return context

    def get_crop_total_areas(self):
        crop_areas = []
        for crop in Crop.objects.all():
            species = (
                crop.content_object if not crop.has_variety() else crop.content_object.species
            )
            crop_areas.append(
                {
                    "y": crop.area.total_area,
                    "x": str(species),
                }
            )
        plot_data = (
            pd.DataFrame(crop_areas)
            .groupby("x", as_index=False)
            .sum()
            .sort_values(by="y", ascending=False)
            .to_dict(orient="records")
        )
        return plot_data

@require_http_methods(["POST",])
def area_sort_hx(request):
    area_pks_order = request.POST.getlist("area_order")
    areas = []
    print(area_pks_order)
    for idx, area_pk in enumerate(area_pks_order, start=1):
        area = Area.objects.get(pk=area_pk)
        area.order = idx
        area.save()
        areas.append(area)
    return render(request, 'spaces/partials/area_list.html', {'areas': areas})


class LocationDetailView(DetailView):
    model = Location
    context_object_name = "location"


class LocationCreateView(CreateView):
    model = Location
    fields = "__all__"
    success_url = reverse_lazy('spaces:location-list')

class LocationUpdateView(UpdateView):
    model = Location
    fields = "__all__"
    success_url = reverse_lazy('spaces:location-list')

class AreaDetailView(DetailView):
    model = Area
    context_object_name = "area"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["parameters"] = Parameter.objects.all()
        return context


class AreaUpdateView(UpdateView):
    model = Area
    fields = ["location", "name", "width", "length"]

    def get_success_url(self):
        return reverse_lazy("spaces:area-detail", args=[self.object.id])


class AreaCreateView(CreateView):
    model = Area
    fields = ["location", "name", "width", "length"]

    def get_success_url(self):
        return reverse_lazy("spaces:area-detail", args=[self.object.id])

    def get_initial(self):
        initial = super().get_initial()
        initial = initial.copy()
        initial["location"] = self.kwargs["location_id"]
        return initial


class AreaDeleteView(DeleteView):
    model = Area
    success_url = reverse_lazy("spaces:location-list")
