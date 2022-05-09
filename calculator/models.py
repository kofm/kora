"""
Models to store informations relative to a user crop.

They consist of a reference Area, a Specie/Variety combination
"""
from django.db import models
from django.utils.timezone import now
from parameters.models import ParameterValue
from register.models import PlantSpecies, PlantVariety

from spaces.models import Area


class Crop(models.Model):
    """
    Stores a specific crop in relation to a specific Area and consisting of a
    PlantSpecies or PlantVarieties.
    """

    notes = models.CharField(
        max_length=500, help_text="Notes relative to the Crop", blank=True, null=True
    )
    species = models.ForeignKey(PlantSpecies, null=True, on_delete=models.CASCADE)
    variety = models.ForeignKey(PlantVariety, null=True, on_delete=models.CASCADE)
    # TODO: delete GenericForeignKey relation
    area = models.ForeignKey(
        Area,
        on_delete=models.CASCADE,
    )

    def __str__(self) -> str:
        if self.has_variety():
            return f"{self.variety.name} ({self.variety.species.common_name})"
        else:
            return self.species.common_name

    def has_variety(self):
        if self.variety:
            return True
        else:
            return False

    def has_species(self):
        if self.species:
            return True
        else:
            return False

    def set_crop(self, object_id, model):
        if model == "plantvariety":
            variety = PlantVariety.objects.get(pk=object_id)
            self.species = variety.species
            self.variety = variety
        elif model == "plantspecies":
            self.species = PlantSpecies.objects.get(pk=object_id)
            self.variety = None
        else:
            return TypeError
        self.save()


    @property
    def sowing(self):
        sowing = self.management_set.filter(type__code="sowing").last()
        if sowing:
            return sowing.date
        else:
            return None

    @sowing.setter
    def sowing(self, value):
        sowing = self.management_set.filter(type__code="sowing").last()
        if sowing:
            sowing.date = value
            sowing.save()
        else:
            type = ManagementType.objects.get(code="sowing")
            mgmt = Management(crop=self, date=value, type=type)
            mgmt.save()

    @sowing.deleter
    def sowing(self):
        sowing = self.management_set.filter(type__code="sowing").last()
        if sowing:
            sowing.delete()

    @property
    def harvest(self):
        harvest = self.management_set.filter(type__code="harvest").last()
        if harvest:
            return harvest.date
        else:
            return None

    @harvest.setter
    def harvest(self, value):
        harvest = self.management_set.filter(type__code="harvest").last()
        if harvest:
            harvest.date = value
            harvest.save()
        else:
            type = ManagementType.objects.get(code="harvest")
            mgmt = Management(crop=self, date=value, type=type)
            mgmt.save()

    @harvest.deleter
    def harvest(self):
        harvest = self.management_set.filter(type__code="harvest").last()  # type: ignore
        if harvest:
            harvest.delete()

    @property
    def is_current(self):
        if self.sowing and self.sowing < now().date():
            if not self.harvest or self.harvest > now().date():
                return True
        return False

    class Meta:
        ordering = ["species", "variety"]


class ManagementType(models.Model):
    code = models.CharField(max_length=30)
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name


class Management(models.Model):
    type = models.ForeignKey(ManagementType, on_delete=models.PROTECT)
    date = models.DateField()
    crop = models.ForeignKey(Crop, on_delete=models.CASCADE)
    notes = models.TextField(blank=True, null=True)

    def __str__(self) -> str:
        return str(self.date) + " - " + self.type.name


class CropParameter(ParameterValue):
    """
    Stores a Species/VarietalParameter ovveride for specific Crop
    """

    crop = models.ForeignKey(Crop, on_delete=models.CASCADE, related_name="parameters")
