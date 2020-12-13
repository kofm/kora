"""
These are the models related to storage of parameters and field measures
"""
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
    value = models.FloatField()
    url_ref=models.URLField(
            help_text="a url reference for the source of the parameter")

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


class VarietalParameter(models.Model):
    """
    Stores the parameters related to varieties
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
    linked_trait = models.ForeignKey(Trait, on_delete=models.PROTECT)
