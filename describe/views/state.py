"""
State views
"""

from breadcrumbs.utils import detail_breadcrumb, generate_breadcrumbs
from describe.forms import RelatedStateForm
from describe.models import Protocol, State
from describe.tables import RelatedStatesTable
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.template.response import TemplateResponse


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
    breadcrumbs = generate_breadcrumbs(
        request, Protocol, state.trait.protocol, [(state.trait, ""), (state, ""), ("Update", "")]
    )
    context.update(breadcrumbs)
    return TemplateResponse(request, "describe/state_form.html", context)


def relatedstate_delete(request, pk):
    state = get_object_or_404(State, pk=pk)
    related_state = request.GET.get("related_state", None)
    if related_state:
        state.related_states.remove(State.objects.get(pk=related_state))
    return HttpResponse()
