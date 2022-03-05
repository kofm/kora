from django.db.models.query_utils import Q
from django.http.response import Http404, HttpResponse, HttpResponseBadRequest, JsonResponse
from django.shortcuts import render
from register.models import PlantSpecies, PlantVariety
import math
from django.core import serializers

from spaces.models import Area, Location
import json

"""
This function is needed to calculate the number of plants per linear metre,
given a specific width
"""
def get_plants_number(distb, distw, width=1):
    if distb==0 or distw==0:
        return (0, 0, 0)
    rows_per_ridge=math.floor(width/distb)
    rows_per_ridge=1 if rows_per_ridge < 2 else rows_per_ridge
    plants_per_row=math.floor(1/distw)
    plants_per_row=1 if plants_per_row < 2 else plants_per_row
    return(rows_per_ridge, plants_per_row, rows_per_ridge*plants_per_row)

def calculator(request):
    locations=Location.objects.values('pk', 'name')
    areas=Area.objects.values('pk', 'name')
    plantspecies=PlantSpecies.objects.values('pk', 'common_name')
    return render(
        request,
        'calculator/index.html',
        {
            'locations': locations,
            'areas': areas,
            'plantspecies' : plantspecies,
        }
    )

def fetch_area(request):
    if request.POST:
        # Get IDs from POST request
        loc_id=request.POST["loc"]
        areas=Area.objects.filter(location__id=loc_id)
        # Initialize json response dictionary
        # Get the specified parameters for the selected plant species
        return HttpResponse(serializers.serialize('json', areas))
    else:
        return JsonResponse({'response' : 'not found'})

def get_varieties(request):
    if request.method == 'POST':
        if 'plantspecies_id' in request.POST:
            try:
                varieties_list=PlantVariety.objects.filter(species_id=request.POST['plantspecies_id']).order_by('name')
            except:
                raise Http404("Plant Species does not exists")
            data = serializers.serialize('json', varieties_list)
            return JsonResponse(data, safe=False)
    else:
        return HttpResponseBadRequest('<h1>Page not found</h1>')
