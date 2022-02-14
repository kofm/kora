from django.http.response import JsonResponse
from django.shortcuts import render
from django.core import serializers

from spaces.models import Area

def calculator(request):
    areas=Area.objects.all()
    return render(request, 'calculator/index.html', { 'areas': areas})

def get_area_ajax(request):
    print("Here")
    if request.method == 'POST':
        area_id=request.POST['area_id']
        try:
            area=Area.objects.filter(pk=area_id)
        except Exception:
            data['error_message']='error'
            return JsonResponse(data)
        data = serializers.serialize("json", area)
        return JsonResponse(data, safe=False)
