"""
Trait
"""

from django.db.models import Max
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.views.decorators.http import require_GET, require_POST

from describe.forms import RelatedStateForm, StateFormSet, TraitForm
from describe.models import Protocol, Trait


@require_GET
def related_state_form(request):
    """Return one field of the form for choosing a related state depending on which parameters are being sent.

    If the request contains `trait` send the `related_state` field; otherwise send the `trait` field.
    This allow building a dynamic form via htmx.
    """
    if request.headers.get("HX-Request") == "true":
        form = RelatedStateForm(request.GET)
        if request.GET.get("trait", None):
            return HttpResponse(form["related_state"])
        else:
            return HttpResponse(form["trait"])


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


@require_POST
def trait_delete(request, pk):
    trait = get_object_or_404(Trait, pk=pk)
    trait.delete()
    trait_next = trait.get_previous_in_protocol() or Trait.objects.filter(protocol=trait.protocol).first()
    if trait_next:
        return redirect(reverse("describe:trait_update", args=(trait_next.pk,)))
    return redirect(reverse("describe:trait_create", args=(trait.protocol.pk,)))
