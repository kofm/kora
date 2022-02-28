from django.db.models.query_utils import Q
from django.http.response import Http404, HttpResponseBadRequest, JsonResponse
from django.shortcuts import render
from register.models import PlantSpecies, PlantVariety
import math
from django.core import serializers

from spaces.models import Area

def get_plants_number(distb, distw, width=1):
    if distb==0 or distw==0:
        return (0, 0, 0)
    rows_per_ridge=math.floor(width/distb)
    rows_per_ridge=1 if rows_per_ridge < 2 else rows_per_ridge
    plants_per_row=math.floor(1/distw)
    plants_per_row=1 if plants_per_row < 2 else plants_per_row
    return(rows_per_ridge, plants_per_row, rows_per_ridge*plants_per_row)

def calculator(request):
    areas=Area.objects.values('pk', 'name')
    plantspecies=PlantSpecies.objects.values('pk', 'common_name')
    return render(
        request,
        'calculator/index.html',
        {
            'areas': areas,
            'plantspecies' : plantspecies,
        }
    )

def get_area_ajax(request):
    if request.method == 'POST':
        # Get IDs from POST request
        area_id=request.POST['area_id']
        plantspecies_id=request.POST['plantspecies_id']
        # import pdb; pdb.set_trace()
        try:
            area=Area.objects.values('length', 'width', 'name').get(pk=area_id)
        except Area.DoesNotExist:
            raise Http404("Area does not exists")
        try:
            plantspecies=PlantSpecies.objects.get(pk=plantspecies_id)
        except PlantSpecies.DoesNotExist:
            raise Http404("Plant Species does not exists")

        # Initialize json response dictionary
        json_resp={}

        # Area is returned as a dictionary
        json_resp=area
        json_resp["total_area"]=round(json_resp["length"]*json_resp["width"],0)

        # These are the parameters being fetched from the species
        fetched_parameters = ["yield", "distw", "distb"]

        # Get the specified parameters for the selected plant species
        params=plantspecies.cropparameter_set.filter(parameter__code__in=fetched_parameters)
        # Now filter out the most recent parameters, at first ordering by update date
        # then get distinct values based on parameter code;
        # finally iterate over the resulting QuerySet and assign value to the
        # json response dictionary
        for prm in params.order_by('parameter__code', 'updated_at').distinct('parameter__code'):
            json_resp[prm.parameter.code]=prm.value

        for prm in fetched_parameters:
            if not prm in json_resp:
                return JsonResponse(json_resp,safe=False)
        # Calculated values from the fetched data
        _, _, json_resp["plant_number_1m"]=get_plants_number(
            json_resp['distb'],
            json_resp['distw']
        )
        json_resp["unit_yield"]=json_resp['yield']/json_resp['plant_number_1m']
        json_resp["nrow"], json_resp["nplants"], json_resp["plant_number"]=get_plants_number(
            json_resp['distb'],
            json_resp['distw'],
            json_resp['width']
        )
        json_resp["expected_yield"]=round(json_resp["unit_yield"]*json_resp["plant_number"]*json_resp["length"],2)
        # Return data in json format
        return JsonResponse(json_resp,safe=False)
    else:
        return HttpResponseBadRequest('<h1>Page not found</h1>')

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
