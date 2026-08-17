from math import ceil, floor

from django.contrib import messages
from django.contrib.auth.decorators import permission_required
from django.db import transaction
from django.db.models import F
from django.http import HttpResponseBadRequest
from django.shortcuts import get_object_or_404, redirect
from django.template.response import TemplateResponse
from django.urls import reverse
from django.views.decorators.http import require_GET, require_POST
from django_tables2 import RequestConfig

from breadcrumbs.utils import add_parent_breadcrumbs, generate_breadcrumbs
from calculator.forms import (
    FieldBookDisplayForm,
    FieldBookForm,
    ParameterTargetForm,
    ParameterTargetObservationForm,
    StepUpdateOrderForm,
    TraitObservationInStepCreateForm,
    TraitTargetForm,
    TraitTargetObservationForm,
)
from calculator.layouts import FieldBookCardLayout, FieldBookGrid
from calculator.models import (
    CropLayout,
    FieldBook,
    ParameterObservation,
    ParameterTarget,
    Step,
    TraitObservation,
    TraitTarget,
)
from calculator.tables import ParameterObservationTable, TraitObservationTable
from calculator.utils import generate_zigzag_pairs
from calculator.views.generic import BaseTargetCreate, BaseTargetDelete
from describe.models import State, Trait
from frontpage.headers import DetailHeader
from frontpage.navigation import BasePrevNextNav
from frontpage.utils.assets import add_layout_assets
from frontpage.utils.htmx import htmx_response_trigger, htmx_response_trigger_close_modal
from frontpage.views_decorators import is_htmx

try:
    from cropmodels.init import AVAILABLE_CROP_MODELS, STATISTICS_MODELS
except ImportError:
    AVAILABLE_CROP_MODELS = []
    STATISTICS_MODELS = []


@permission_required("calculator.view_fieldbook", raise_exception=True)
def fieldbook_list(request, layout_id):
    layout = get_object_or_404(CropLayout, pk=layout_id)
    cards = FieldBookCardLayout(layout.fieldbooks.all())
    return TemplateResponse(
        request,
        "calculator/fieldbook/fieldbook_list.html",
        {"layout": layout, "cards": cards, "nav_fieldbook": "active"},
    )


@permission_required("calculator.add_fieldbook", raise_exception=True)
def fieldbook_create(request, layout_id):
    layout = get_object_or_404(CropLayout.objects.visible(), pk=layout_id)
    form = FieldBookForm(request.POST or None)
    form.fields.pop("layout")

    if form.is_valid():
        fieldbook = form.save(commit=False)
        fieldbook.layout = layout
        fieldbook.save()
        if is_htmx(request):
            return htmx_response_trigger_close_modal(["fieldbooksUpdated"])
        return redirect(f"{layout.get_absolute_url()}?tab=fieldbooks")

    template_name = "frontpage/modal_form.html" if is_htmx(request) else "frontpage/_create_form.html"
    return TemplateResponse(
        request,
        template_name,
        {"form": form, "model_name": "Field book", "object_to_create": "Fieldbook"},
    )


@permission_required("calculator.view_fieldbook", raise_exception=True)
def fieldbook_detail(request, pk):
    fieldbook = get_object_or_404(FieldBook.objects.select_related("layout"), pk=pk)
    crops = fieldbook.layout.crops.prefetch_related("variety__species").order_by("order")
    is_read_only = fieldbook.layout.is_archived

    highlighted = request.GET.get("highlighted")

    plots_layout = FieldBookGrid(
        crops,
        fieldbook=fieldbook,
        highlighted=highlighted,
        selectable=request.user.has_perm("calculator.change_fieldbook") and not is_read_only,
    )

    if is_htmx(request):
        return TemplateResponse(
            request,
            "calculator/fieldbook/detail.html#steps",
            {"plots_layout": plots_layout, "is_read_only": is_read_only},
        )

    trait_target_form = TraitTargetForm()
    parameter_target_form = ParameterTargetForm()
    display_form = FieldBookDisplayForm(
        initial={"display_config": fieldbook.get_display_config_string()} or {}, fieldbook=fieldbook
    )
    order_form = StepUpdateOrderForm()

    breadcrumbs = generate_breadcrumbs(request, FieldBook, fieldbook)
    breadcrumbs = add_parent_breadcrumbs(breadcrumbs, fieldbook.layout)
    header = DetailHeader(request, fieldbook, title=fieldbook.name, subtitle=fieldbook.layout.name)
    context = {
        "fieldbook": fieldbook,
        "header": header,
        "plots_layout": plots_layout,
        "trait_target_form": trait_target_form,
        "parameter_target_form": parameter_target_form,
        "display_form": display_form,
        "order_form": order_form,
        "is_read_only": is_read_only,
        **breadcrumbs,
    }
    add_layout_assets(context, plots_layout)

    return TemplateResponse(request, "calculator/fieldbook/detail.html", context)


@require_POST
@permission_required("calculator.change_fieldbook", raise_exception=True)
def fieldbook_update_display_config(request, pk):
    fieldbook = get_object_or_404(
        FieldBook.objects.select_related("layout"),
        pk=pk,
    )
    initial = {"display_config": fieldbook.get_display_config_string()}
    display_form = FieldBookDisplayForm(request.POST, initial=initial, fieldbook=fieldbook)
    if display_form.is_valid():
        display_form.save()
    return redirect(reverse("calculator:fieldbook_detail", args=(fieldbook.pk,)))


@require_POST
@permission_required("calculator.change_fieldbook", raise_exception=True)
def fieldbook_update_step_order(request, pk):
    fieldbook = get_object_or_404(
        FieldBook.objects.mutable().select_related("layout"),
        pk=pk,
    )
    form = StepUpdateOrderForm(request.POST)
    if form.is_valid():
        ncol = fieldbook.layout.ncol
        start_corner = form.cleaned_data["start_corner"]
        block_width = min(ncol, form.cleaned_data["block_width"])
        crops = fieldbook.layout.crops.order_by("order")
        steps = Step.objects.filter(fieldbook_id=fieldbook.pk)
        steps_by_crop_map = {step.crop_id: step for step in steps}

        layout = {}
        nrows = ceil(len(crops) / ncol)
        for idx, crop in enumerate(crops):
            x = idx % ncol + 1
            y = floor(idx / ncol) + 1
            layout[(x, y)] = crop
        order = 0
        for coord in generate_zigzag_pairs(ncol, nrows, block_width, start_corner):
            crop = layout.get(coord)
            if crop is None:
                continue
            step = steps_by_crop_map.get(crop.pk)
            if step:
                step.order = order
                order += 1
        Step.objects.bulk_update(steps_by_crop_map.values(), ["order"])

    return redirect(reverse("calculator:fieldbook_detail", args=(fieldbook.pk,)))


class TraitTargetCreate(BaseTargetCreate):
    model = TraitTarget
    form_class = TraitTargetForm
    field_name = "trait"

    def get_compatible_crops_and_count(self, selected_crops, target_obj):
        compatible_crops = [
            crop for crop in selected_crops if crop.variety.species_id == target_obj.protocol.plantspecies_id
        ]
        skipped_crop_count = len(selected_crops) - len(compatible_crops)
        return compatible_crops, skipped_crop_count


class ParameterTargetCreate(BaseTargetCreate):
    model = ParameterTarget
    form_class = ParameterTargetForm
    field_name = "parameter"


class TraitTargetDelete(BaseTargetDelete):
    model = TraitTarget

    def has_observation(self, target):
        return target.step.traitobservation.filter(state__trait_id=target.trait_id).exists()


class ParameterTargetDelete(BaseTargetDelete):
    model = ParameterTarget

    def has_observation(self, target):
        return target.step.parameterobservation.filter(parameter_id=target.parameter_id).exists()


@require_POST
@permission_required("calculator.change_fieldbook", raise_exception=True)
def fieldbook_targets_delete(request, fieldbook_id):
    selection = request.POST.getlist("selection")
    if not selection:
        return HttpResponseBadRequest()

    fieldbook = get_object_or_404(
        FieldBook.objects.mutable().select_related("layout"),
        pk=fieldbook_id,
    )
    selected_crop_ids = set(fieldbook.layout.crops.filter(pk__in=selection).values_list("pk", flat=True))
    if len(selected_crop_ids) != len(set(selection)):
        return HttpResponseBadRequest()

    selected_steps = Step.objects.filter(fieldbook=fieldbook, crop_id__in=selected_crop_ids)
    observed_trait_targets = TraitTarget.objects.filter(
        step__in=selected_steps,
        step__traitobservation__state__trait_id=F("trait_id"),
    ).distinct()
    observed_parameter_targets = ParameterTarget.objects.filter(
        step__in=selected_steps,
        step__parameterobservation__parameter_id=F("parameter_id"),
    ).distinct()

    with transaction.atomic():
        retained_target_count = observed_trait_targets.count() + observed_parameter_targets.count()
        removable_trait_targets = TraitTarget.objects.filter(step__in=selected_steps).exclude(
            pk__in=observed_trait_targets.values("pk")
        )
        removable_parameter_targets = ParameterTarget.objects.filter(step__in=selected_steps).exclude(
            pk__in=observed_parameter_targets.values("pk")
        )
        removed_target_count = removable_trait_targets.count() + removable_parameter_targets.count()
        removable_trait_targets.delete()
        removable_parameter_targets.delete()

        selected_steps.filter(
            traittarget__isnull=True,
            parametertarget__isnull=True,
            traitobservation__isnull=True,
            parameterobservation__isnull=True,
        ).delete()

        display_config = fieldbook.display_config
        if display_config:
            target_model = TraitTarget if display_config["model"] == "trait" else ParameterTarget
            field_name = display_config["model"]
            if not target_model.objects.filter(
                step__fieldbook=fieldbook,
                **{f"{field_name}_id": display_config["id"]},
            ).exists():
                fieldbook.display_config = None
                fieldbook.save(update_fields=["display_config"])

    messages.success(
        request,
        f"{removed_target_count} target{'s' if removed_target_count != 1 else ''} removed from the fieldbook.",
    )
    if retained_target_count:
        messages.warning(request, "Some targets were not removed because they have already been observed.")

    return redirect(reverse("calculator:fieldbook_detail", args=(fieldbook.pk,)))


def get_step(pk):
    return get_object_or_404(
        Step.objects.select_related("fieldbook__layout__location", "crop__variety__species").prefetch_related(
            "traittarget__trait"
        ),
        pk=pk,
    )


def build_step_trait_targets_context(step):
    observed_traits_ids = (
        TraitObservation.objects.filter(step=step).values_list("state__trait_id", flat=True).distinct()
    )
    target_traits = step.traittarget.exclude(trait__in=observed_traits_ids)
    target_traits_ids = target_traits.values_list("trait_id", flat=True)
    trait_map = Trait.objects.filter(pk__in=target_traits_ids).in_bulk()
    states_by_trait_map = State.objects.filter(trait__in=target_traits_ids).trait_dict()

    trait_forms = []
    for target in target_traits:
        states = states_by_trait_map.get(target.trait_id)
        form = TraitTargetObservationForm(states=states)
        form.fields["state"].label = str(trait_map.get(target.trait_id))
        form.delete_url = reverse("calculator:trait_target_delete", args=(target.pk,))
        trait_forms.append(form)

    return {"step": step, "trait_forms": trait_forms, "is_read_only": step.fieldbook.layout.is_archived}


def build_step_parameter_targets_context(step):
    observed_parameter_ids = (
        ParameterObservation.objects.filter(step=step).values_list("parameter_id", flat=True).distinct()
    )
    parameter_targets = (
        ParameterTarget.objects.select_related("parameter")
        .filter(step=step)
        .exclude(parameter_id__in=observed_parameter_ids)
    )

    parameter_forms = []
    for target in parameter_targets:
        form = ParameterTargetObservationForm(
            initial={"parameter": target.parameter_id},
            form_title=target.parameter.name,
        )
        form.delete_url = reverse("calculator:parameter_target_delete", args=(target.pk,))
        parameter_forms.append(form)

    return {"step": step, "parameter_forms": parameter_forms, "is_read_only": step.fieldbook.layout.is_archived}


def build_step_trait_observations_context(request, step):
    observations = TraitObservation.objects.select_related("state__trait", "created_by").filter(step=step)
    table = TraitObservationTable(
        observations,
        prefix="traits-",
        is_read_only=step.fieldbook.layout.is_archived,
    )
    table.htmx_url = reverse("calculator:step_trait_observations", args=(step.pk,))
    RequestConfig(request, paginate={"per_page": 10}).configure(table)
    return {"trait_observations_table": table, "is_read_only": step.fieldbook.layout.is_archived}


def build_step_parameter_observations_context(request, step):
    observations = ParameterObservation.objects.select_related("parameter", "created_by").filter(step=step)
    table = ParameterObservationTable(
        observations,
        prefix="parameters-",
        is_read_only=step.fieldbook.layout.is_archived,
    )
    table.htmx_url = reverse("calculator:step_parameter_observations", args=(step.pk,))
    RequestConfig(request, paginate={"per_page": 10}).configure(table)
    return {"parameter_observations_table": table, "is_read_only": step.fieldbook.layout.is_archived}


@permission_required("calculator.view_step", raise_exception=True)
def step_detail(request, pk):
    step = get_step(pk)
    step_nav = BasePrevNextNav(step)
    breadcrumbs = generate_breadcrumbs(request, Step, step)
    breadcrumbs = add_parent_breadcrumbs(breadcrumbs, step.crop)
    breadcrumbs = add_parent_breadcrumbs(breadcrumbs, step.fieldbook)
    breadcrumbs = add_parent_breadcrumbs(breadcrumbs, step.fieldbook.layout)
    context = {
        "step": step,
        "step_nav": step_nav,
        **build_step_trait_targets_context(step),
        **build_step_parameter_targets_context(step),
        **build_step_trait_observations_context(request, step),
        **build_step_parameter_observations_context(request, step),
        **breadcrumbs,
    }
    return TemplateResponse(request, "calculator/step/detail.html", context)


@require_GET
@permission_required("calculator.view_step", raise_exception=True)
def step_trait_targets(request, pk):
    step = get_step(pk)
    return TemplateResponse(
        request,
        "calculator/step/detail.html#trait_targets",
        build_step_trait_targets_context(step),
    )


@require_GET
@permission_required("calculator.view_step", raise_exception=True)
def step_parameter_targets(request, pk):
    step = get_step(pk)
    return TemplateResponse(
        request,
        "calculator/step/detail.html#parameter_targets",
        build_step_parameter_targets_context(step),
    )


@require_GET
@permission_required("calculator.view_step", raise_exception=True)
def step_trait_observations(request, pk):
    step = get_step(pk)
    return TemplateResponse(
        request,
        "calculator/step/detail.html#trait_observations_table",
        build_step_trait_observations_context(request, step),
    )


@require_GET
@permission_required("calculator.view_step", raise_exception=True)
def step_parameter_observations(request, pk):
    step = get_step(pk)
    return TemplateResponse(
        request,
        "calculator/step/detail.html#parameter_observations_table",
        build_step_parameter_observations_context(request, step),
    )


@require_POST
@permission_required("calculator.add_traitobservation", raise_exception=True)
def trait_observation_in_step_create(request, step_id):
    step = get_object_or_404(
        Step.objects.mutable().select_related("fieldbook__layout", "crop"),
        pk=step_id,
    )
    form = TraitObservationInStepCreateForm(request.POST)
    if form.is_valid():
        obs = form.save(commit=False)
        if not TraitTarget.objects.filter(step=step, trait__states=obs.state).exists():
            return HttpResponseBadRequest()
        obs.step = step
        obs.crop = step.crop
        obs.created_by = request.user
        obs.save()
    if is_htmx(request):
        return htmx_response_trigger(["traitObservationUpdated"])
    return redirect(reverse("calculator:step_detail", args=(step.pk,)))


@require_POST
@permission_required("calculator.add_parameterobservation", raise_exception=True)
def parameter_observation_in_step_create(request, step_id):
    step = get_object_or_404(
        Step.objects.mutable().select_related("fieldbook__layout", "crop"),
        pk=step_id,
    )
    form = ParameterTargetObservationForm(request.POST)
    if form.is_valid():
        get_object_or_404(ParameterTarget, step=step, parameter=form.cleaned_data["parameter"])
        instance = form.save(commit=False)
        instance.created_by = request.user
        instance.crop_id = step.crop_id
        instance.step = step
        instance.save()
        if is_htmx(request):
            return htmx_response_trigger(["observationParameterUpdated"])
    return redirect(reverse("calculator:step_detail", args=(step.pk,)))
