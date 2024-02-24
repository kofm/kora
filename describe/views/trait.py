"""
Trait
"""

from django.http import HttpResponse
from django.views.decorators.http import require_GET
from describe.forms import RelatedStateForm


@require_GET
def related_state_form(request):
    """Return one field of the form for choosing a related state depending on which parameters are being sent.

    If the request contains `trait` send the `related_state` field; otherwise send the `trait` field.
    This allow building a dynamic form via htmx.
    """
    if request.htmx:
        form = RelatedStateForm(request.GET)
        if request.GET.get("trait", None):
            return HttpResponse(form["related_state"])
        else:
            return HttpResponse(form["trait"])
