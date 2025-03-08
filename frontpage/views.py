from django.http import HttpResponse
from django.shortcuts import render


def index(request):
    return render(request, "frontpage/index.html", {"nav_home": "active", "crumbs": None})


def appearance_set(request):
    appearance = request.POST.get("appearance", "light")
    print(request.POST)
    request.session["appearance"] = appearance
    print(request.session["appearance"])
    return HttpResponse()
