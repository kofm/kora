import json

from django.http import HttpResponse


def htmx_response_trigger(triggers: list):
    return HttpResponse(headers={"HX-Trigger": json.dumps(dict.fromkeys(triggers, True))})


def htmx_response_trigger_close_modal(triggers: list):
    trig_dict = {"closeModal": True}
    trig_dict.update(dict.fromkeys(triggers, True))
    return HttpResponse(headers={"HX-Trigger": json.dumps(trig_dict)})


def htmx_response_redirect(url):
    return HttpResponse(headers={"HX-Redirect": url})
