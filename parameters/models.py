"""
These are the models related to storage of parameters and field measures
"""
from django.db import models
from django.urls import reverse
from register.models import PlantSpecies, PlantVariety


class ParameterManager(models.Manager):
    def get_by_natural_key(self, code):
        return self.get(code=code)


class Parameter(models.Model):
    """
    Stores the parameters related to the Species. Parameters are inputs on which Crop
    Models rely on. This class defines the available parameters. The actual values are
    stored in ParameterValue objects, that reference one Parameter.
    """

    code = models.CharField(
        max_length=50, help_text="A code to identify the parameter.", unique=True
    )
    name = models.CharField(max_length=200, help_text="The name of the parameter.")
    description = models.CharField(
        max_length=200, help_text="The description of the parameter."
    )
    measure_unit = models.CharField(max_length=50, help_text="The unit of measurement.")

    objects = ParameterManager()

    def __str__(self):
        return self.code

    def get_absolute_url(self):
        return reverse(
            "parameters:parameter-detail",
            args=[
                self.pk,
            ],
        )

    def natural_key(self):
        return (self.code,)


class ParameterValue(models.Model):
    """
    Abstract class for parameters values
    """

    value = models.FloatField()
    url_ref = models.URLField(
        help_text="a url reference for the source of the parameter",
        blank=True,
        null=True,
    )
    parameter = models.ForeignKey(Parameter, on_delete=models.RESTRICT)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    note = models.CharField(
        max_length=512, blank=True, help_text="Add any additional information here."
    )

    class Meta:
        abstract = True

    def __str__(self):
        return self.parameter.code


class SpeciesParameter(ParameterValue):
    """
    Crop parameters values
    """

    specie = models.ForeignKey(
        PlantSpecies, on_delete=models.RESTRICT, related_name="parameters"
    )


class VarietalParameter(ParameterValue):
    """
    Varietal parameters values
    """

    variety = models.ForeignKey(
        PlantVariety, on_delete=models.RESTRICT, related_name="parameters"
    )
