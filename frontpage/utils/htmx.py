import json

from django.http import HttpResponse


def htmx_response_trigger(triggers: list):
    return HttpResponse(headers={"HX-Trigger": json.dumps({trigger: True for trigger in triggers})})


def htmx_response_trigger_close_modal(triggers: list):
    trig_dict = {"closeModal": True}
    trig_dict.update({trigger: True for trigger in triggers})
    return HttpResponse(headers={"HX-Trigger": json.dumps(trig_dict)})


def htmx_response_redirect(url):
    return HttpResponse(headers={"HX-Redirect": url})
