"""
Models to store informations relative to a user crop.

They consist of a reference Area, a Specie/Variety combination
"""
from django.db import models

class Crop(models.Model):
    """
    Stores a specific crop in relation to a specific Area and consisting of a
    PlantSpecies or Varieties. It can store temporary ovverides e.g. for the
    temperature offset of the Area, or planting scheme (distw, distb)
    """
    notes=models.CharField(max_length=500, help_text="Notes relative to the Crop")
