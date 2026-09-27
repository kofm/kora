from decimal import Decimal
from typing import Any

from django.contrib.auth.decorators import permission_required
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.db.models import Count
from django.shortcuts import get_object_or_404, redirect
from django.template.response import TemplateResponse
from django.urls import reverse
from django.utils.html import format_html
from django.views.generic.edit import UpdateView
from django_tables2.config import RequestConfig

from breadcrumbs.utils import generate_breadcrumbs
from calculator.tables import CropLayoutTable
from frontpage.autocomplete import AutocompleteModelView
from frontpage.headers import DetailHeader, ListHeader
from frontpage.utils.htmx import htmx_response_redirect, htmx_response_trigger_close_modal
from frontpage.views_decorators import htmx_render_blocks, is_htmx
from spaces.filters import LocationFilter
from spaces.forms import LocationForm
from spaces.models import Location
from spaces.tables import LocationTable


class LocationAutocompleteView(AutocompleteModelView):
    model = Location
    ordering = ["name", "pk"]


@permission_required("spaces.view_location")
@htmx_render_blocks(["main"])
def location_list(request):
    context: dict[str, Any] = {}
    flt = LocationFilter(request.GET, Location.objects.all())
    table = LocationTable(flt.qs)
    RequestConfig(request, paginate={"per_page": 12}).configure(table)
    context["header"] = ListHeader(request, Location, modal=True)
    context.update({"table": table, "filter": flt, **generate_breadcrumbs(request, Location)})
    return TemplateResponse(request, "spaces/location_list.html", context)


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
    lat = location.latitude
    lon = location.longitude
    coords = ""
    if lat is not None and lon is not None:
        coords = format_html(
            '<a class="row-link text-decoration-none link-body-emphasis text-muted" '
            'href="https://www.openstreetmap.org/?mlat={}&mlon={}#map=15/{}/{}" '
            'target="_blank" rel="noopener noreferrer">{}, {}</a>',
            lat,
            lon,
            lat,
            lon,
            f"{Decimal(str(lat)):.4f}",
            f"{Decimal(str(lon)):.4f}",
        )
    context = {
        "location": location,
        "coords": coords,
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
            return htmx_response_trigger_close_modal(["resultsChanged"])
        return redirect(reverse("spaces:location_list"))
    return TemplateResponse(
        request,
        "frontpage/modal_form.html",
        {"object_to_create": "Location", "form": form},
    )


class LocationUpdateView(PermissionRequiredMixin, UpdateView):
    model = Location
    fields = ("name", "latitude", "longitude")
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
