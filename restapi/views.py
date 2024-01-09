from django.shortcuts import get_object_or_404
from rest_framework import viewsets
from describe.models import Protocol
from parameters.models import VarietalParameter
from collect.models import SeedSample, StoragePosition

from register.models import Entity, PlantSpecies, PlantVariety, Protection
from restapi.serializers import (
    EntitySerializer,
    PlantSpeciesSerializer,
    PlantVarietySerializer,
    ProtectionSerializer,
    ProtocolSerializer,
    SeedSampleSerializer,
    StoragePositionSerializer,
    VarietalParameterSerializer,
)


class PlantSpeciesViewSet(viewsets.ModelViewSet):
    """
    API endpoint to view/edit a Crop
    """

    queryset = PlantSpecies.objects.all()
    serializer_class = PlantSpeciesSerializer


class PlantVarietyViewSet(viewsets.ModelViewSet):
    queryset = PlantVariety.objects.all()
    serializer_class = PlantVarietySerializer

    def get_queryset(self):
        species = self.request.query_params.get("species", None)
        queryset = PlantVariety.objects.all()
        if species is not None:
            queryset = queryset.filter(species=species)
        return queryset


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


class StoragePositionViewSet(viewsets.ModelViewSet):
    queryset = StoragePosition.objects.all()
    serializer_class = StoragePositionSerializer


class ProtocolViewSet(viewsets.ModelViewSet):
    queryset = Protocol.objects.all()
    serializer_class = ProtocolSerializer

    def get_queryset(self):
        variety_id = self.request.query_params.get("variety", None)
        if variety_id is not None:
            variety = get_object_or_404(PlantVariety, pk=variety_id)
            return Protocol.objects.filter(plantspecies=variety.species)
        return Protocol.objects.all()
