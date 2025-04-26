from django.http import HttpResponse
from django.template.response import TemplateResponse


def index(request):
    return TemplateResponse(request, "frontpage/index.html", {"nav_home": "active", "crumbs": None})


def appearance_set(request):
    appearance = request.POST.get("appearance", "light")
    request.session["appearance"] = appearance
    return HttpResponse()
