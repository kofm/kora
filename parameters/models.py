"""
These are the models related to storage of parameters and field measures
"""
from django.db import models

from describe.models import Trait
from register.models import PlantSpecies, PlantVariety

class Parameter(models.Model):
    """
    Stores the parameters related to the Species
    """

    code = models.CharField(
        max_length=50, help_text="A code to identify the parameter."
    )
    name = models.CharField(max_length=200, help_text="The name of the parameter.")
    description = models.CharField(
        max_length=200, help_text="The description of the parameter."
    )
    measure_unit = models.CharField(max_length=50, help_text="The unit of measurement.")

    def __str__(self):
        return self.code

class ParameterValue(models.Model):
    """
    Abstract class for parameters values
    """

    value = models.FloatField()
    url_ref = models.URLField(
        help_text="a url reference for the source of the parameter"
    )
    parameter = models.ForeignKey(Parameter, on_delete=models.RESTRICT)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        """
        This is an abstract class
        """
        abstract = True

    def __str__(self):
        return self.parameter.code

class SpeciesParameter(ParameterValue):
    """
    Crop parameters values
    """
    specie = models.ForeignKey(PlantSpecies, on_delete=models.RESTRICT)

class VarietalParameter(ParameterValue):
    """
    Varietal parameters values
    """
    variety = models.ForeignKey(PlantVariety, on_delete=models.RESTRICT)

class Measure(models.Model):
    """
    Stores the measures related to a variety
    """
    georeference_lat = models.FloatField()
    georeference_lon = models.FloatField()
    measure_unit = models.CharField(max_length=50)
    value = models.FloatField()
    variety = models.ForeignKey(PlantVariety, on_delete=models.RESTRICT)
    trait = models.ForeignKey(Trait, on_delete=models.PROTECT)
