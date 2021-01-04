from django.shortcuts import render

# Create your views here.
def index(request):
    context={}
    context["nav_home"] = "active"
    return render(request, 'frontpage/index.html', context)
