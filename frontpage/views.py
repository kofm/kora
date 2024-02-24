from django.http import HttpResponse
from django.shortcuts import render


def index(request):
    context = {}
    context["nav_home"] = "active"
    return render(request, "frontpage/index.html", context)


def darkmode_toggle(request):
    is_light = request.session.get("is_light", False)
    request.session["is_light"] = not is_light
    return HttpResponse()
