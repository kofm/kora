from django.http import HttpResponse
from django.shortcuts import render


def index(request):
    context = {}
    context["nav_home"] = "active"
    return render(request, "frontpage/index.html", context)


def darkmode_toggle(request):
    is_dark = request.session.get("is_dark", False)
    request.session["is_dark"] = not is_dark
    return HttpResponse()
