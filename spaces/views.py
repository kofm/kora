from django.contrib.auth.decorators import permission_required
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.db.models import Count
from django.shortcuts import get_object_or_404, redirect
from django.template.response import TemplateResponse
from django.urls import reverse
from django.views.generic.edit import UpdateView
from django_tables2.config import RequestConfig

from breadcrumbs.utils import generate_breadcrumbs
from calculator.tables import CropLayoutTable
from django_sortable_htmx.views import SortableView
from frontpage.autocomplete import AutocompleteModelView
from frontpage.headers import DetailHeader, ListHeader
from frontpage.utils.htmx import htmx_response_redirect, htmx_response_trigger_close_modal
from frontpage.views_decorators import htmx_render_blocks, is_htmx
from spaces.forms import LocationForm
from spaces.models import Location


class LocationAutocompleteView(AutocompleteModelView):
    model = Location
    ordering = ["order", "name"]


@permission_required("spaces.view_location")
def location_list(request):
    context = {}
    context["object_list"] = Location.objects.all().order_by("order", "name")
    if is_htmx(request):
        return TemplateResponse(request, "spaces/location_list.html#sortable", context)
    header = ListHeader(request, Location, modal=True)
    context.update({"header": header, **generate_breadcrumbs(request, Location)})
    return TemplateResponse(request, "spaces/location_list.html", context)


class SortLocation(SortableView):
    model = Location


@permission_required("spaces.view_location")
@htmx_render_blocks(["layouts"])
def location_detail(request, pk):
    location = get_object_or_404(Location, pk=pk)
    layouts = location.crop_layouts.visible().annotate(
        crop_count=Count("crops", distinct=True),
        fieldbook_count=Count("fieldbooks", distinct=True),
    )
    table = CropLayoutTable(layouts)
    RequestConfig(request).configure(table)
    header = DetailHeader(request, location, delete_modal=True)
    context = {
        "location": location,
        "table": table,
        "header": header,
        **generate_breadcrumbs(request, Location, location),
    }
    return TemplateResponse(request, "spaces/location_detail.html", context)


@permission_required("spaces.add_location", raise_exception=True)
def location_create(request):
    form = LocationForm(request.POST or None)
    if form.is_valid():
        form.save()
        if is_htmx(request):
            return htmx_response_trigger_close_modal(["LocationUpdated"])
        return redirect(reverse("spaces:location_list"))
    return TemplateResponse(
        request,
        "frontpage/modal_form.html",
        {"object_to_create": "Location", "form": form},
    )


class LocationUpdateView(PermissionRequiredMixin, UpdateView):
    model = Location
    fields = "__all__"
    permission_required = ["spaces.change_location"]

    def get_success_url(self):
        return reverse("spaces:location_detail", args=(self.object.pk,))


@permission_required("spaces.delete_location", raise_exception=True)
def location_delete(request, pk):
    location = get_object_or_404(Location, pk=pk)
    if request.method == "POST" and location.is_deletable:
        location.delete()
        return htmx_response_redirect(reverse("spaces:location_list"))
    return TemplateResponse(request, "frontpage/modal_confirm_delete.html", {"instance": location})
