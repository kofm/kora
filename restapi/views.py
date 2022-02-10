from register.models import PlantSpecies
from rest_framework import viewsets
from restapi.serializers import CropSerializer

class CropViewSet(viewsets.ModelViewSet):
    """
    API endpoint to view/edit a Crop
    """
    queryset = PlantSpecies.objects.all()
    serializer_class = CropSerializer




