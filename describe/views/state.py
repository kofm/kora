"""
State views
"""

from django.contrib.auth.decorators import permission_required
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.template.response import TemplateResponse
from django.urls import reverse
from django.views.decorators.http import require_GET, require_POST

from breadcrumbs.utils import generate_breadcrumbs
from describe.forms import RelatedStateForm, StateForm
from describe.models import Protocol, State, Trait
from describe.tables import RelatedStatesTable


@require_POST
@permission_required("describe.add_state", raise_exception=True)
def state_create(request):
    form = StateForm(request.POST)
    if form.is_valid():
        form.save()
    return render(request, "describe/partials/state_form.html", {"form": form})


@require_GET
@permission_required("describe.add_state", raise_exception=True)
def state_form(request, trait_pk):
    trait = get_object_or_404(Trait, pk=trait_pk)
    form = StateForm(initial={"trait": trait})
    return render(request, "describe/partials/state_form.html", {"form": form})


@permission_required("describe.change_state", raise_exception=True)
def state_update(request, pk):
    state = get_object_or_404(State, pk=pk)
    form = RelatedStateForm(initial={"state": state.pk})
    if request.method == "POST":
        form = RelatedStateForm(request.POST)
        if form.is_valid():
            related_state = State.objects.get(pk=form["related_state"].value())
            state.related_states.add(related_state)
    table = RelatedStatesTable(state.related_states.all())
    context = {"state": state, "object": state, "table": table, "form": form}
    state_crumbs = [(state.trait, ""), (state, ""), ("Update", "")]
    breadcrumbs = generate_breadcrumbs(request, Protocol, state.trait.protocol, state_crumbs)
    context.update(breadcrumbs)
    return TemplateResponse(request, "describe/state_form.html", context)


@require_POST
@permission_required("describe.delete_state", raise_exception=True)
def state_delete(request, pk):
    state = get_object_or_404(State, pk=pk)
    state.delete()
    return redirect(reverse("describe:trait_update", args=(state.trait.pk,)))


@permission_required("describe.change_state", raise_exception=True)
def relatedstate_delete(request, pk):
    state = get_object_or_404(State, pk=pk)
    related_state = request.GET.get("related_state", None)
    if related_state:
        state.related_states.remove(State.objects.get(pk=related_state))
    return HttpResponse()
