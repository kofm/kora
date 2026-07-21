from django.contrib import messages
from django.contrib.auth.decorators import permission_required
from django.db import transaction
from django.db.models import Count, Max, Q
from django.http import Http404, HttpResponse, HttpResponseBadRequest
from django.shortcuts import get_object_or_404, redirect, render
from django.template.response import TemplateResponse
from django.urls import reverse
from django.views.decorators.http import require_http_methods

from breadcrumbs.utils import add_parent_breadcrumbs, generate_breadcrumbs
from describe.forms import StateFormSet, TraitForm, TraitStatesForm
from describe.models import (
    PREFETCHED_RELATED_STATES_ATTR_NAME,
    Protocol,
    State,
    StateGroup,
    Trait,
)
from frontpage.utils.htmx import htmx_response_trigger
from frontpage.views_decorators import is_htmx


@permission_required("describe.add_trait", raise_exception=True)
def trait_create(request, protocol_pk):
    protocol = get_object_or_404(Protocol, pk=protocol_pk)
    if request.method == "POST":
        form = TraitForm(request.POST)
        if form.is_valid():
            trait = form.save()
            return redirect(reverse("describe:trait_update", args=(trait.pk,)))
    else:
        numeric_id__max = protocol.traits.aggregate(Max("numeric_id"))["numeric_id__max"]
        form = TraitForm(initial={"protocol": protocol, "numeric_id": numeric_id__max + 1})
    return render(request, "describe/partials/trait_form.html", {"form": form, "protocol": protocol, "oob": True})


@permission_required("describe.change_trait", raise_exception=True)
@transaction.atomic
def trait_update(request, pk):
    trait = get_object_or_404(Trait, pk=pk)
    trait_prev = trait.get_previous_in_protocol()
    trait_next = trait.get_next_in_protocol()
    form = TraitForm(instance=trait)
    formset = StateFormSet(instance=trait)
    if request.method == "POST":
        form = TraitForm(request.POST, instance=trait)
        formset = StateFormSet(request.POST, instance=trait)
        if formset.is_valid():
            formset.save()
            # Return the updated formset without validation and with
            # an extra empty field.
            formset = StateFormSet(instance=trait)
        if form.is_valid():
            form.save()
    return render(
        request,
        "describe/partials/trait_form.html",
        {
            "current_trait": trait,
            "form": form,
            "formset": formset,
            "oob": True,
            "protocol": trait.protocol,
            "trait_prev": trait_prev,
            "trait_next": trait_next,
        },
    )


@require_http_methods(["POST"])
@permission_required("describe.delete_trait", raise_exception=True)
def trait_delete(request, pk):
    trait = get_object_or_404(Trait, pk=pk)
    trait.delete()
    trait_next = trait.get_previous_in_protocol() or Trait.objects.filter(protocol=trait.protocol).first()
    if trait_next:
        return redirect(reverse("describe:trait_update", args=(trait_next.pk,)))
    return redirect(reverse("describe:trait_create", args=(trait.protocol.pk,)))


@permission_required("describe.change_trait", raise_exception=True)
def trait_relate_states(request, pk):
    context = {}
    trait = get_object_or_404(Trait.objects.select_related("protocol").prefetch_related("states"), pk=pk)
    context["trait"] = trait
    trait_states = trait.states_with_related_states()
    context["target_states"] = trait_states

    for parent_state in trait_states:
        parent_state.directly_related_state_ids = {
            state.pk
            for state in getattr(
                parent_state,
                PREFETCHED_RELATED_STATES_ATTR_NAME,
                [],
            )
        }

    if is_htmx(request):
        template_partial = "describe/trait_relate_states.html#target_states"
        return TemplateResponse(request, template_partial, context)

    context["form"] = TraitStatesForm()

    # These URLs are needed for the protocol and trait `TomSelect`
    # inputs, respectively.
    plantspecies_id = trait.protocol.plantspecies_id
    protocol_query = {"plantspecies": plantspecies_id, "exclude_id": trait.protocol_id}
    context["protocols_list_url"] = reverse("restapi:protocols-list", query=protocol_query)
    context["traits_list_url"] = f"{reverse('restapi:traits-list')}"

    crumbs = generate_breadcrumbs(request, Trait, trait)
    crumbs = add_parent_breadcrumbs(crumbs, trait.protocol)
    context.update(crumbs)

    return TemplateResponse(request, "describe/trait_relate_states.html", context)


@require_http_methods(["POST"])
@permission_required("describe.change_trait", raise_exception=True)
def state_sortable_source_list(request):
    """Return a source state list-group partial, that constitute the GUI for relating states.

    If `trait` is not available in the POST request, return an empty list group partial."""

    if not is_htmx(request):
        return Http404()

    # The form may submit an empty `trait_id` value, so we need to
    # send back an empty partial.
    trait_id = request.POST.get("trait")
    if not trait_id:
        return render(
            request,
            "describe/trait_relate_states.html#states_list",
            {},
        )

    trait = get_object_or_404(Trait, pk=trait_id)
    states = State.objects.select_related("trait__protocol").filter(trait=trait)
    return render(
        request,
        "describe/trait_relate_states.html#states_list",
        {"states": states},
    )


@require_http_methods(["POST"])
@permission_required("describe.change_trait", raise_exception=True)
@transaction.atomic
def state_related_states_update(request, pk):
    try:
        target_state_id = int(request.POST["target_state_id"])
    except (KeyError, TypeError, ValueError):
        return HttpResponseBadRequest()

    source_state = get_object_or_404(State.objects.select_related("trait"), pk=pk)
    target_state = get_object_or_404(State.objects.select_related("trait"), pk=target_state_id)

    if source_state == target_state.id:
        messages.warning(request, "You can't relate a state with itself.")
    elif source_state.group_id == target_state.group_id:
        messages.warning(request, "This relation is already specified.")
    elif (
        source_state.trait.protocol_id == target_state.trait.protocol_id
        and source_state.trait_id != target_state.trait_id
    ):
        messages.warning(request, "Merging states from different traits in the same protocol is not supported.")
    else:
        target_state.related_states.add(source_state)
        State.objects.filter(group_id=source_state.group_id).update(group_id=target_state.group_id)
        StateGroup.objects.filter(states__isnull=True).delete()
        messages.success(request, "Relation updated.")

    return htmx_response_trigger(["target-states-changed"])


@require_http_methods(["POST"])
@transaction.atomic
@permission_required("describe.change_trait", raise_exception=True)
def state_related_states_delete(request, pk):
    try:
        target_state_id = int(request.POST["target_state_id"])
    except (KeyError, TypeError, ValueError):
        return HttpResponseBadRequest()
    source = get_object_or_404(State, pk=pk)
    target = get_object_or_404(State, pk=target_state_id)
    group_id = source.group_id
    source.related_states.remove(target)

    # After deleting a relation, groups (aka cached connected
    # components) need to be rebuilded
    State.objects.filter(group=group_id).rebuild_groups()

    return htmx_response_trigger(["target-states-changed"])


@require_http_methods(["POST"])
@transaction.atomic
@permission_required("describe.change_trait", raise_exception=True)
def state_related_states_bulk_delete(request, pk):
    state = get_object_or_404(State, pk=pk)
    group_id = state.group_id
    group_state_ids = State.objects.filter(group_id=state.group_id).values_list("pk", flat=True)
    related_in_group = State.objects.filter(pk__in=group_state_ids, related_states=state)
    state.related_states.remove(*related_in_group)
    State.objects.filter(group=group_id).rebuild_groups()
    return htmx_response_trigger(["target-states-changed"])


@require_http_methods(["POST"])
@transaction.atomic
@permission_required("describe.change_trait", raise_exception=True)
def trait_states_related_states_reset(request, pk):
    trait = get_object_or_404(Trait.objects.select_related("protocol").prefetch_related("states"), pk=pk)

    # We leave the out the states in a singleton group with
    # `group_size__gt=1`
    trait_state_ids = (
        trait.states_with_related_states()
        .annotate(group_size=Count("group__states"))
        .filter(group_size__gt=1)
        .values_list("id", flat=True)
    )
    if not trait_state_ids:
        return HttpResponse(status=204)

    affected_group_ids = list(
        State.objects.filter(pk__in=trait_state_ids).values_list("group_id", flat=True).distinct()
    )

    through = State.related_states.through
    through.objects.filter(Q(from_state_id__in=trait_state_ids) | Q(to_state_id__in=trait_state_ids)).delete()
    State.objects.filter(group_id__in=affected_group_ids).rebuild_groups()

    return htmx_response_trigger(["target-states-changed"])


@require_http_methods(["POST"])
@transaction.atomic
def trait_states_bulk_relate(request, pk):
    """Relate states from a source trait to a target trait by pairing them one by one, until possible."""

    target_trait = get_object_or_404(Trait, pk=pk)
    source_trait_id = request.POST.get("trait")
    if not source_trait_id:
        return HttpResponseBadRequest()

    source_trait = get_object_or_404(Trait, pk=source_trait_id)
    target_states = list(target_trait.states.select_related("group").order_by("numeric_id", "pk"))
    source_states = list(source_trait.states.order_by("numeric_id", "pk"))
    pairs = [
        (source_state, target_state)
        for source_state, target_state in zip(source_states, target_states, strict=False)
        if source_state.pk != target_state.pk
    ]
    if not pairs:
        return HttpResponseBadRequest()

    through = State.related_states.through
    relations = [
        through(from_state_id=source_state.pk, to_state_id=target_state.pk) for source_state, target_state in pairs
    ]
    # Also add the inverse of the relations, to match symmetrical=True of the related_states M2M property
    relations.extend(
        through(from_state_id=target_state.pk, to_state_id=source_state.pk) for source_state, target_state in pairs
    )
    through.objects.bulk_create(relations, ignore_conflicts=True, batch_size=1000)

    affected_group_ids = {state.group_id for pair in pairs for state in pair}
    State.objects.filter(group_id__in=affected_group_ids).rebuild_groups()

    messages.success(request, "States succesfully mapped by position.")
    response = HttpResponse()
    response["HX-Trigger"] = "target-states-changed"
    return response
