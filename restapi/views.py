from rest_framework import viewsets

from register.models import PlantSpecies, PlantVariety
from restapi.serializers import PlantSpeciesSerializer, PlantVarietySerializer

class CropViewSet(viewsets.ModelViewSet):
    """
    API endpoint to view/edit a Crop
    """

    queryset = PlantSpecies.objects.all()
    serializer_class = PlantSpeciesSerializer

class PlantVarietyViewSet(viewsets.ModelViewSet):
    queryset = PlantVariety.objects.all()
    serializer_class = PlantVarietySerializer
