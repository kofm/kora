import json

from django.http import HttpResponse


def htmx_trigger_response(triggers: list):
    return HttpResponse(headers={"HX-Trigger": json.dumps({trigger: True for trigger in triggers})})


def htmx_trigger_response_close_modal(triggers: list):
    trig_dict = {"closeModal": True}
    trig_dict.update({trigger: True for trigger in triggers})
    return HttpResponse(headers={"HX-Trigger": json.dumps(trig_dict)})
