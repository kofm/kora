from django.http.response import JsonResponse
from django.shortcuts import render
from django.core import serializers
from register.models import PlantSpecies

from spaces.models import Area

def calculator(request):
    areas=Area.objects.all()
    plantspecies=PlantSpecies.objects.all()
    return render(request, 'calculator/index.html', { 'areas': areas, 'plantspecies' : plantspecies})

def get_area_ajax(request):
    if request.method == 'POST':
        area_id=request.POST['area_id']
        plantspecies_id=request.POST['plantspecies_id']
        try:
            area=Area.objects.filter(pk=area_id).first()
            plantspecies=PlantSpecies.objects.filter(pk=plantspecies_id).first()
            yld=plantspecies.cropparameter_set.filter(parameter__code="yield").first()
            objects = [area, yld]
        except Exception:
            data['error_message']='error'
            return JsonResponse(data)
        data = serializers.serialize("json", objects)
        return JsonResponse(data, safe=False)

def ajax_test(request):
    return JsonResponse({'test': 'test', 'a': 1 }, safe=False)
