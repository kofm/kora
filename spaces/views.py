import json

from django.db.models.base import Model
from django.shortcuts import get_object_or_404
from django.template.response import TemplateResponse
from django.urls import reverse
from django.urls.base import reverse_lazy
from django.views.decorators.http import require_http_methods
from django.views.generic import DetailView
from django.views.generic.edit import CreateView, DeleteView, UpdateView

from breadcrumbs.utils import add_parent_breadcrumbs, generate_breadcrumbs
from django_sortable_htmx.views import SortableView
from frontpage.utils.htmx import htmx_response_redirect, htmx_response_trigger_close_modal
from frontpage.views_decorators import htmx_render_blocks, nav_active
from spaces.forms import AreaForm
from spaces.models import Area, Location


def location_list(request):
    queryset = Location.objects.all().order_by("order", "name")
    context = {
        "object_list": queryset,
        **generate_breadcrumbs(request, Location),
    }
    return TemplateResponse(request, "spaces/location_list.html", context)


class SortLocation(SortableView):
    model = Location


@require_http_methods(["POST"])
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


@htmx_render_blocks(["areas"])
def location_detail(request, pk):
    location = get_object_or_404(Location, pk=pk)

    context = {
        "location": location,
        **generate_breadcrumbs(request, Location, location),
    }
    return TemplateResponse(request, "spaces/location_detail.html", context)


class LocationCreateView(CreateView):
    model = Location
    fields = ["name", "latitude", "longitude"]
    success_url = reverse_lazy("spaces:location_list")


def area_create(request, location_id):
    location = get_object_or_404(Location, pk=location_id)
    if request.method == "POST":
        form = AreaForm(request.POST)
        if form.is_valid():
            area = form.save(commit=False)
            area.location = location
            area.save()
            return htmx_response_trigger_close_modal(["areaUpdated"])
    else:
        form = AreaForm()

    context = {"form": form, "object_to_create": "Area"}
    return TemplateResponse(request, "frontpage/modal_form.html", context)


class LocationUpdateView(UpdateView):
    model = Location
    fields = "__all__"

    def get_success_url(self):
        return reverse("spaces:location-detail", args=(self.object.pk,))


class LocationDeleteView(DeleteView):
    model = Location
    success_url = reverse_lazy("spaces:location_list")


class AreaDetailView(DetailView):
    model = Area
    context_object_name = "area"


@nav_active("nav_plan")
def area_detail(request, pk):
    area = Area.objects.select_related("location").get(pk=pk)

    breadcrumbs = generate_breadcrumbs(request, Area, area)
    breadcrumbs = add_parent_breadcrumbs(breadcrumbs, area.location)
    context = {"area": area, **breadcrumbs}
    return TemplateResponse(request, "spaces/area_detail.html", context)


def duplicate_object(object: Model):
    object.pk = None
    object._state.adding = True
    return object


def area_duplicate(request, pk):
    area = Area.objects.values("width", "length", "location_id").get(pk=pk)
    if request.method == "POST":
        form = AreaForm(request.POST, initial=area)
        if form.is_valid():
            created_area = form.save(commit=False)
            created_area.location_id = area["location_id"]
            created_area.save()
            response = htmx_response_redirect(reverse("spaces:area-detail", args=(created_area.pk,)))
            response.headers["HX-Trigger"] = json.dumps({"closeModal": True})
            return response
    else:
        form = AreaForm(initial=area)
    return TemplateResponse(
        request, "frontpage/modal_form.html", {"area": area, "object_to_create": "Area", "form": form}
    )


class AreaSort(SortableView):
    model = Area


class AreaUpdateView(UpdateView):
    model = Area
    fields = ["location", "name", "width", "length"]

    def get_success_url(self):
        return reverse_lazy("spaces:area-detail", args=[self.object.id])


class AreaDeleteView(DeleteView):
    model = Area
    success_url = reverse_lazy("spaces:location_list")
