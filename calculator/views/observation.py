from django.contrib.auth.decorators import permission_required
from django.shortcuts import get_object_or_404
from django.template.response import TemplateResponse
from django.urls import reverse
from django.views.decorators.http import require_POST
from django_tables2 import RequestConfig

from breadcrumbs.utils import breadcrumbs_context
from calculator.filters import ParameterObservationFilter, TraitObservationFilter
from calculator.forms import (
    ObservationParameterForm,
    ParameterObservationUpdateForm,
    TraitObservationCreateForm,
    TraitObservationUpdateForm,
)
from calculator.models import Crop, ParameterObservation, TraitObservation
from calculator.tables import ParameterObservationListTable, TraitObservationListTable
from describe.models import State
from frontpage.utils.htmx import htmx_response_trigger_close_modal
from frontpage.views_decorators import htmx_render_blocks, nav_active


@permission_required("calculator.view_traitobservation", raise_exception=True)
@nav_active("nav_plan")
@htmx_render_blocks(["main"])
def trait_observation_list(request):
    queryset = TraitObservation.objects.select_related(
        "crop__layout",
        "crop__variety__species",
        "state__trait__protocol",
        "created_by",
    ).order_by("-recorded_at", "-pk")
    observation_filter = TraitObservationFilter(request.GET, queryset=queryset)
    table = TraitObservationListTable(observation_filter.qs)
    RequestConfig(request, paginate={"per_page": 15}).configure(table)
    context = {
        "filter": observation_filter,
        "table": table,
        **breadcrumbs_context([("Trait observations", reverse("calculator:trait_observation_list"))]),
    }
    return TemplateResponse(request, "calculator/trait_observation_list.html", context)


@permission_required("calculator.view_parameterobservation", raise_exception=True)
@nav_active("nav_plan")
@htmx_render_blocks(["main"])
def parameter_observation_list(request):
    queryset = ParameterObservation.objects.select_related(
        "crop__layout",
        "crop__variety__species",
        "parameter",
        "created_by",
    ).order_by("-recorded_at", "-pk")
    observation_filter = ParameterObservationFilter(request.GET, queryset=queryset)
    table = ParameterObservationListTable(observation_filter.qs)
    RequestConfig(request, paginate={"per_page": 15}).configure(table)
    context = {
        "filter": observation_filter,
        "table": table,
        **breadcrumbs_context([("Parameter observations", reverse("calculator:parameter_observation_list"))]),
    }
    return TemplateResponse(request, "calculator/parameter_observation_list.html", context)


@permission_required("calculator.add_traitobservation", raise_exception=True)
def trait_observation_create(request, crop_id):
    crop = get_object_or_404(
        Crop.objects.mutable().select_related("variety__species"),
        pk=crop_id,
    )
    form = TraitObservationCreateForm(request.POST or None, crop=crop)
    if form.is_valid():
        observation = form.save(commit=False)
        observation.crop = crop
        observation.created_by = request.user
        observation.save()
        return htmx_response_trigger_close_modal(["traitObservationUpdated"])
    return TemplateResponse(request, "frontpage/modal_form.html", {"form": form})


@permission_required("calculator.change_traitobservation", raise_exception=True)
def trait_observation_update(request, pk):
    instance = get_object_or_404(
        TraitObservation.objects.mutable().select_related("state__trait__protocol"),
        pk=pk,
    )
    states = State.objects.filter(trait=instance.trait_id)
    if request.method == "POST":
        form = TraitObservationUpdateForm(request.POST, instance=instance)
        form.fields["state"].queryset = states
        if form.is_valid():
            form.save()
            return htmx_response_trigger_close_modal(["traitObservationUpdated"])
    else:
        form = TraitObservationUpdateForm(instance=instance)
        form.fields["state"].queryset = states
    context = {"form": form, "instance": instance}
    return TemplateResponse(request, "calculator/trait_observation_update.html", context)


@permission_required("calculator.delete_traitobservation", raise_exception=True)
@require_POST
def trait_observation_delete(request, pk):
    instance = get_object_or_404(
        TraitObservation.objects.mutable().select_related("state"),
        pk=pk,
    )
    instance.delete()
    return htmx_response_trigger_close_modal(["traitObservationUpdated"])


@permission_required("calculator.add_parameterobservation", raise_exception=True)
def parameter_observation_create(request, crop_id):
    crop = get_object_or_404(
        Crop.objects.mutable().select_related("variety"),
        pk=crop_id,
    )
    if request.method == "POST":
        form = ObservationParameterForm(request.POST)
        if form.is_valid():
            obs = form.save(commit=False)
            obs.crop = crop
            obs.created_by = request.user
            obs.save()
            return htmx_response_trigger_close_modal(["observationParameterUpdated"])
    else:
        form = ObservationParameterForm()
    return TemplateResponse(request, "frontpage/modal_form.html", {"form": form})


@permission_required("calculator.change_parameterobservation", raise_exception=True)
def parameter_observation_update(request, pk):
    instance = get_object_or_404(
        ParameterObservation.objects.mutable().select_related("parameter"),
        pk=pk,
    )
    form = ParameterObservationUpdateForm(request.POST or None, instance=instance)
    if request.method == "POST" and form.is_valid():
        form.save()
        return htmx_response_trigger_close_modal(["observationParameterUpdated"])
    return TemplateResponse(
        request,
        "calculator/parameter_observation_update.html",
        {"form": form, "instance": instance},
    )


@permission_required("calculator.delete_parameterobservation", raise_exception=True)
@require_POST
def parameter_observation_delete(request, pk):
    instance = get_object_or_404(ParameterObservation.objects.mutable(), pk=pk)
    instance.delete()
    return htmx_response_trigger_close_modal(["observationParameterUpdated"])
