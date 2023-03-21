from django.db.models.base import Model
from django.db.models.expressions import F
from django.shortcuts import get_object_or_404, redirect, render
from django.template.response import TemplateResponse
from django.urls.base import reverse_lazy
from django.views.decorators.http import require_http_methods
from django.views.generic import DetailView, ListView
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from calculator.models import Crop
import pandas as pd
from .utils import get_max_order

from spaces.models import Area, Location


class LocationListView(ListView):
    model = Location

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["crop_total_areas"] = self.get_crop_total_areas()
        return context

    def get_crop_total_areas(self):
        if Crop.objects.exists():
            crop_areas = []
            for crop in Crop.objects.all():
                species = (
                    crop.species if not crop.has_variety() else crop.variety.species
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
        else:
            return None


@require_http_methods(
    [
        "POST",
    ]
)
def area_sort_hx(request):
    area_pks_ordered = request.POST.getlist("area_order")
    location_pk = request.POST.get("location")
    location = Location.objects.get(pk=location_pk)
    area_list = []
    for idx, area_pk in enumerate(area_pks_ordered, start=1):
        area = Area.objects.get(pk=area_pk)
        area.order = idx
        area.location = location
        area.save()
        area_list.append(area)
    return TemplateResponse(
        request,
        "spaces/partials/area_list.html",
        {"area_list": area_list, "location": location},
    )


def location_detail(request, pk):
    """
    Returns the detail view of a Location.
    `order_by` defines the order of the within-location areas
    `sortable` disable sorting (using Sortable.js) if any sorting methods is
    selected by the user. Defaults to True so the user can arrange Area cards
    to their liking
    """
    order_by = request.GET.get("order_by")
    location = get_object_or_404(Location, pk=pk)
    areas = location.area_set.all()
    sortable = "true"
    if order_by:
        sortable = "false"
        if order_by == "area":
            areas = areas.order_by(F("length") * F("width"))
        else:
            areas = areas.order_by(order_by)

    context = {
        "sortable": sortable,
        "location": location,
        "areas": areas,
        "order_by": order_by,
    }
    return TemplateResponse(request, "spaces/location_detail.html", context)


class LocationCreateView(CreateView):
    model = Location
    fields = "__all__"
    success_url = reverse_lazy("spaces:location-list")


class LocationUpdateView(UpdateView):
    model = Location
    fields = "__all__"
    success_url = reverse_lazy("spaces:location-list")


class LocationDeleteView(DeleteView):
    model = Location
    success_url = reverse_lazy("spaces:location-list")


class AreaDetailView(DetailView):
    model = Area
    context_object_name = "area"


def duplicate_object(object: Model):
    object.pk = None
    object._state.adding = True
    return object


def area_duplicate(request, pk):
    area = get_object_or_404(Area, pk=pk)
    if request.POST:
        new_area = duplicate_object(area)
        new_area.name = new_area.name + " copy"
        new_area.save()
        return redirect(reverse_lazy("spaces:area-update", args=[new_area.pk]))
    return TemplateResponse(
        request,
        "spaces/area_duplicate_confirm.html",
        {
            "area": area,
        },
    )


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

    def form_valid(self, form):
        self.object = form.save(commit=False)
        order = get_max_order(self.object.location)
        self.object.order = order
        self.object.save()
        return super().form_valid(form)


class AreaDeleteView(DeleteView):
    model = Area
    success_url = reverse_lazy("spaces:location-list")


def test(request):
    return render(request, "spaces/test.html")
