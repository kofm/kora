import math
from django.http.response import (
    Http404,
    HttpResponse,
    HttpResponseBadRequest,
    JsonResponse,
)
from django.shortcuts import render
from calculator.models import Crop, CropParameter
from register.models import PlantSpecies, PlantVariety
from django.core import serializers

from spaces.models import Area, Location


def get_plants_number(distb, distw, width=1):
    """
    This function is needed to calculate the number of plants per linear metre,
    given a specific width
    """
    if distb == 0 or distw == 0:
        return (0, 0, 0)
    rows_per_ridge = math.floor(width / distb)
    rows_per_ridge = 1 if rows_per_ridge < 2 else rows_per_ridge
    plants_per_row = math.floor(1 / distw)
    plants_per_row = 1 if plants_per_row < 2 else plants_per_row
    return (rows_per_ridge, plants_per_row, rows_per_ridge * plants_per_row)


def calculator(request):
    locations = Location.objects.values("pk", "name")
    plantspecies = PlantSpecies.objects.values("pk", "common_name")
    return render(
        request,
        "calculator/index.html",
        {
            "locations": locations,
            "plantspecies": plantspecies,
        },
    )


def fetch_area(request):
    """
    This is the endpoint to get all the Area associated to a specific
    location, given its ID.
    It returns a serialized object.
    """
    if request.POST:
        # Get location id from POST request
        loc_id = request.POST["loc"]
        # Fetch all areas for that location
        areas = Area.objects.filter(location__id=loc_id)
        # Return serialized object
        return HttpResponse(serializers.serialize("json", areas))
    else:
        return JsonResponse({"error": ""}, status=400)


def fetch_species(request):
    if request.POST:
        species_id = request.POST["species"]
        varieties = PlantVariety.objects.filter(species__id=species_id)
        species_params = PlantSpecies.objects.get(
            pk=species_id
        ).speciesparameter_set.filter(parameter__code__in=["distw", "distb", "yield"])
        all_objects = [*varieties, *species_params]
        return HttpResponse(
            serializers.serialize(
                "json",
                all_objects,
                use_natural_primary_keys=True,
                use_natural_foreign_keys=True,
            )
        )
    else:
        return JsonResponse({"error": ""}, status=400)


def store(request):
    if request.POST:
        species = PlantSpecies.objects.get(pk=request.POST["species_id"])
        area = Area.objects.get(pk=request.POST["area_id"])
        crop = Crop(content_object=species, area=area, notes="")
        crop.save()
        des = serializers.deserialize("json", request.POST.get("crop_params"))
        for d in des:
            cp = CropParameter(
                value=d.object.value,
                parameter=d.object.parameter,
                url_ref="https://mater.cc",
                crop=crop,
            )
            cp.save()
        return HttpResponse({"result": "ok"}, status=200)
    else:
        return JsonResponse({"error": ""}, status=400)
