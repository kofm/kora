from rest_framework import viewsets

from register.models import PlantSpecies
from restapi.serializers import PlantSpeciesSerializer

class CropViewSet(viewsets.ModelViewSet):
    """
    API endpoint to view/edit a Crop
    """

    queryset = PlantSpecies.objects.all()
    serializer_class = PlantSpeciesSerializer
