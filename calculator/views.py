from django.contrib.contenttypes.models import ContentType
from django.forms.models import ModelForm
from django.http.response import (
    HttpResponse,
    JsonResponse,
)
from django.shortcuts import redirect, render
from django.core import serializers
from django.urls.base import reverse, reverse_lazy
from django.views.generic.detail import DetailView
from django.views.generic.edit import DeleteView, UpdateView
from rest_framework.decorators import api_view
from rest_framework import status
from rest_framework.response import Response
from calculator.serializers import AreaSerializer, CropParameterSerializer
from calculator.models import Crop, CropParameter
from parameters.models import Parameter
from register.models import PlantSpecies, PlantVariety
from spaces.models import Area, Location

"""Register CropModels here"""
CROP_MODELS = [
    'CropModelExpectedYield',
    'CropModelTotalPlants'
]

class CropDetailView(DetailView):
    model = Crop


class CropDeleteView(DeleteView):
    model = Crop
    success_url = reverse_lazy("spaces:locations_list")


class CropUpdateView(UpdateView):
    model = Crop
    fields = ["area", "notes"]

    def get_success_url(self):
        return reverse_lazy("calculator:crop-update", args=[self.object.id])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["plantspecies"] = PlantSpecies.objects.all()
        context["parameters"] = Parameter.objects.all()
        # Get possible content_types
        plantspecies = ContentType.objects.get(
            app_label="register", model="plantspecies"
        )
        if self.object.content_type == plantspecies:
            context["plantspecie"] = self.object.object_id
        import importlib; module = importlib.import_module('calculator.cropmodels')
        context['cropmodels'] = []
        for cm in CROP_MODELS:
            class_ = getattr(module, cm)
            m = class_(self.object)
            if m.can_run():
                context['cropmodels'].append(m.output())
        return context


class CropParameterForm(ModelForm):
    class Meta:
        model = CropParameter
        fields = ["parameter", "value", "crop"]


def cropparameter_update(request):
    if request.POST:
        form = CropParameterForm(request.POST)
        if form.is_valid():
            CropParameter.objects.update_or_create(
                crop=form.cleaned_data["crop"],
                parameter=form.cleaned_data["parameter"],
                defaults={"value": form.cleaned_data["value"]},
            )
    return redirect("calculator:crop-update", request.POST["crop"])


def index(request):
    locations = Location.objects.values("pk", "name")
    plantspecies = PlantSpecies.objects.values("pk", "common_name")
    crops = Crop.objects.all()
    return render(
        request,
        "calculator/index.html",
        {"locations": locations, "plantspecies": plantspecies, "crops": crops},
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


@api_view(["GET", "POST"])
def cropparameter_list(request):
    if request.method == "GET":
        snippets = CropParameter.objects.all()
        serializer = CropParameterSerializer(snippets, many=True)
        return Response(serializer.data)

    elif request.method == "POST":
        serializer = CropParameterSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["DELETE"])
def cropparameter_detail(request, pk):
    try:
        cropparameter = CropParameter.objects.get(pk=pk)
    except CropParameter.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == "DELETE":
        cropparameter.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
