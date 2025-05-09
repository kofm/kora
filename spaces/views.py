from django.contrib.auth.decorators import permission_required
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.shortcuts import get_object_or_404
from django.template.response import TemplateResponse
from django.urls import reverse
from django.urls.base import reverse_lazy
from django.views.generic.edit import CreateView, DeleteView, UpdateView

from breadcrumbs.utils import add_parent_breadcrumbs, generate_breadcrumbs
from django_sortable_htmx.views import SortableView
from frontpage.utils.htmx import htmx_response_trigger_close_modal
from frontpage.views_decorators import htmx_render_blocks, nav_active
from spaces.forms import AreaForm
from spaces.models import Area, Location


@permission_required("spaces.view_location")
def location_list(request):
    queryset = Location.objects.all().order_by("order", "name")
    context = {
        "object_list": queryset,
        **generate_breadcrumbs(request, Location),
    }
    return TemplateResponse(request, "spaces/location_list.html", context)


class SortLocation(SortableView):
    model = Location


@permission_required("spaces.view_location")
@htmx_render_blocks(["areas"])
def location_detail(request, pk):
    location = get_object_or_404(Location, pk=pk)

    context = {
        "location": location,
        **generate_breadcrumbs(request, Location, location),
    }
    return TemplateResponse(request, "spaces/location_detail.html", context)


class LocationCreateView(PermissionRequiredMixin, CreateView):
    model = Location
    fields = ["name", "latitude", "longitude"]
    success_url = reverse_lazy("spaces:location_list")
    permission_required = ["spaces.add_location"]


@permission_required("spaces.add_area")
def area_create(request, location_id):
    location = get_object_or_404(Location, pk=location_id)
    duplicate = request.GET.get("duplicate", None)
    try:
        initial = Area.objects.values("name", "width", "length", "location_id").get(pk=duplicate) if duplicate else {}
    except Area.DoesNotExist:
        initial = {}
    if request.method == "POST":
        form = AreaForm(request.POST, initial=initial)
        if form.is_valid():
            area = form.save(commit=False)
            area.location = location
            area.save()
            return htmx_response_trigger_close_modal(["areaUpdated"])
    else:
        form = AreaForm(initial=initial)

    context = {"form": form, "object_to_create": "Area"}
    return TemplateResponse(request, "frontpage/modal_form.html", context)


class LocationUpdateView(PermissionRequiredMixin, UpdateView):
    model = Location
    fields = "__all__"
    permission_required = ["spaces.change_location"]

    def get_success_url(self):
        return reverse("spaces:location_detail", args=(self.object.pk,))


class LocationDeleteView(PermissionRequiredMixin, DeleteView):
    model = Location
    success_url = reverse_lazy("spaces:location_list")
    permission_required = ["spaces.delete_location"]


@nav_active("nav_plan")
@permission_required("spaces.view_area")
def area_detail(request, pk):
    area = Area.objects.select_related("location").get(pk=pk)

    breadcrumbs = generate_breadcrumbs(request, Area, area)
    breadcrumbs = add_parent_breadcrumbs(breadcrumbs, area.location)
    context = {"area": area, **breadcrumbs}
    return TemplateResponse(request, "spaces/area_detail.html", context)


class AreaSort(PermissionRequiredMixin, SortableView):
    model = Area
    permission_required = ["spaces.change_area"]


class AreaUpdateView(PermissionRequiredMixin, UpdateView):
    model = Area
    fields = ("location", "name", "width", "length")
    permission_required = ["spaces.change_area"]

    def get_success_url(self):
        return reverse_lazy("spaces:area_detail", args=(self.object.id,))


class AreaDeleteView(PermissionRequiredMixin, DeleteView):
    model = Area
    success_url = reverse_lazy("spaces:location_list")
    permission_required = ["spaces.delete_area"]
