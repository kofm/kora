"""
Trait
"""


from django.http import HttpResponse
from describe.forms import RelatedStateForm


def trait_list_htmx(request):
    """
    This is accessed by HTMX requests made by RelatedStateForm to populate the
    Trait/State select input, depending on the selected Protocol/Trait
    """
    if request.htmx:
        form = RelatedStateForm(request.GET)
        if "protocol" in request.GET:
            return HttpResponse(form["trait"])
        else:
            return HttpResponse(form["related_state"])
