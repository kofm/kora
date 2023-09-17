from django.shortcuts import render


def index(request):
    context = {}
    context["nav_home"] = "active"
    return render(request, "frontpage/index.html", context)
