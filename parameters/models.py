"""
These are the models related to storage of parameters and field measures
"""
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models
from register.models import PlantSpecies,PlantVariety
from describe.models import Trait


class Parameter(models.Model):
    """
    Stores the parameters related to the Species
    """
    name=models.CharField(
            max_length=200,
            help_text="the name of the parameter"
            )
    measure_unit = models.CharField(max_length=50)

    class Meta:
        """
        Meta
        """
        abstract = True

class CropParameter(Parameter):
    """
    Stores the parameters related to species
    """
    specie = models.ForeignKey(PlantSpecies,on_delete=models.RESTRICT)


class VarietalParameter(Parameter):
    """
    Stores the parameters related to varieties
    """
    variety = models.ForeignKey(PlantVariety, on_delete=models.RESTRICT)

class ParameterValue(models.Model):
    """
    Abstract class for parameters values
    """
    value = models.FloatField()
    url_ref=models.URLField(
                    help_text="a url reference for the source of the parameter"
                    )

    class Meta:
        """
        This is an abstract class
        """
        abstract = True


class CropParameterValue(ParameterValue):
    """
    Crop parameters values
    """
    parameter = models.ForeignKey(CropParameter, on_delete=models.RESTRICT)

class VarietalParameterValue(ParameterValue):
    """
    Varietal parameters values
    """
    parameter = models.ForeignKey(VarietalParameter, on_delete=models.RESTRICT)

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
