from rest_framework import viewsets
from parameters.models import VarietalParameter
from collect.models import SeedSample

from register.models import Entity, PlantSpecies, PlantVariety, Protection
from restapi.serializers import EntitySerializer, PlantSpeciesSerializer, PlantVarietySerializer, ProtectionSerializer, SeedSampleSerializer, VarietalParameterSerializer


class CropViewSet(viewsets.ModelViewSet):
    """
    API endpoint to view/edit a Crop
    """

    queryset = PlantSpecies.objects.all()
    serializer_class = PlantSpeciesSerializer


class PlantVarietyViewSet(viewsets.ModelViewSet):
    queryset = PlantVariety.objects.all()
    serializer_class = PlantVarietySerializer


class EntityViewSet(viewsets.ModelViewSet):
    queryset = Entity.objects.all()
    serializer_class = EntitySerializer

class ProtectionViewSet(viewsets.ModelViewSet):
    queryset = Protection.objects.all()
    serializer_class = ProtectionSerializer

class VarietalParameterViewSet(viewsets.ModelViewSet):
    queryset = VarietalParameter.objects.all()
    serializer_class = VarietalParameterSerializer


class SeedSampleViewSet(viewsets.ModelViewSet):
    queryset = SeedSample.objects.all()
    serializer_class = SeedSampleSerializer
