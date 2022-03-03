"""
Models to store informations relative to a user crop.

They consist of a reference Area, a Specie/Variety combination
"""
from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from parameters.models import ParameterValue

from spaces.models import Area

class Crop(models.Model):
    """
    Stores a specific crop in relation to a specific Area and consisting of a
    PlantSpecies or Varieties. It can store temporary ovverides e.g. for the
    temperature offset of the Area, or planting scheme (distw, distb)
    """
    notes=models.CharField(max_length=500, help_text="Notes relative to the Crop")
    # Relation to PlantSpecies or PlantVariety
    content_type=models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id=models.PositiveIntegerField()
    content_object=GenericForeignKey('content_type', 'object_id')
    area=models.ForeignKey(Area, on_delete=models.PROTECT,)

    def __str__(self) -> str:
        if self.content_type.model=='plantspecies':
            return self.content_object.common_name
        else:
            return self.content_object.name

class CropParameter(ParameterValue):
    """
    Stores a Species/VarietalParameter ovveride for specific Crop
    """
    crop=models.ForeignKey(Crop, on_delete=models.CASCADE)
