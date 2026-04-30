from django.contrib.auth.decorators import permission_required
from django.db import transaction
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.views.decorators.http import require_http_methods

from describe.forms import StateForm
from describe.models import State, Trait


@require_http_methods(["POST"])
@permission_required("describe.add_state", raise_exception=True)
def state_create(request):
    form = StateForm(request.POST)
    if form.is_valid():
        state = form.save(commit=False)
        state.reset_group()
        state.save()
    return render(request, "describe/partials/state_form.html", {"form": form})


@require_http_methods(["GET"])
@permission_required("describe.add_state", raise_exception=True)
def state_form(request, trait_pk):
    trait = get_object_or_404(Trait, pk=trait_pk)
    form = StateForm(initial={"trait": trait})
    return render(request, "describe/partials/state_form.html", {"form": form})


@require_http_methods(["POST"])
@permission_required("describe.delete_state", raise_exception=True)
@transaction.atomic
def state_delete(request, pk):
    state = get_object_or_404(State.objects.select_related("group"), pk=pk)
    state.group.delete()
    state.delete()
    return redirect(reverse("describe:trait_update", args=(state.trait.pk,)))
