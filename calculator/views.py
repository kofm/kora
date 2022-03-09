from django.http.response import (
    HttpResponse,
    JsonResponse,
)
from django.shortcuts import render
from django.core import serializers
from rest_framework.decorators import api_view
from rest_framework.response import Response

from calculator.serializers import AreaSerializer

from calculator.models import Crop, CropParameter
from register.models import PlantSpecies, PlantVariety
from spaces.models import Area, Location


def index(request):
    locations = Location.objects.values("pk", "name")
    plantspecies = PlantSpecies.objects.values("pk", "common_name")
    crops = Crop.objects.all()
    return render(
        request,
        "calculator/index.html",
        {
            'locations': locations,
            'plantspecies': plantspecies,
            'crops': crops
        },
    )


@api_view(["GET"])
def fetch_area(request, pk):
    """
    This is the endpoint to get all the Area associated to a specific location, given
    its ID.
    It returns a serialized object.
    """
    if request.method == "GET":
        # Fetch all areas for that location
        areas = Area.objects.filter(location__id=pk)
        # Return serialized objects
        serializer = AreaSerializer(areas, many=True)
        return Response(serializer.data)


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
