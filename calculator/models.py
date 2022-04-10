"""
Models to store informations relative to a user crop.

They consist of a reference Area, a Specie/Variety combination
"""
from datetime import datetime
from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.utils.functional import cached_property
from django.utils.timezone import now
from parameters.models import ParameterValue

from spaces.models import Area


class Crop(models.Model):
    """
    Stores a specific crop in relation to a specific Area and consisting of a
    PlantSpecies or Varieties. It can store temporary ovverides e.g. for the
    temperature offset of the Area, or planting scheme (distw, distb)
    """

    notes = models.CharField(
        max_length=500, help_text="Notes relative to the Crop", blank=True, null=True
    )
    # Relation to PlantSpecies or PlantVariety
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey("content_type", "object_id")
    area = models.ForeignKey(
        Area,
        on_delete=models.PROTECT,
    )

    def __str__(self) -> str:
        if self.content_type.model == "plantspecies":
            return self.content_object.common_name
        else:
            return self.content_object.name + " (" + self.content_object.species.common_name + ")"

    def has_variety(self):
        if self.content_type.model == 'plantvariety':
            return True
        else:
            return False

    def has_species(self):
        if self.content_type.model == 'plantspecies':
            return True
        else:
            return False

    def set_crop(self, object_id, model):
        crop_model = ContentType.objects.get(
            app_label="register", model=model
        )
        self.content_type = crop_model
        self.object_id = object_id

    @property
    def sowing(self):
        sowing = self.management_set.filter(type__code='sowing').last()
        if sowing:
            return sowing.date
        else:
            return None

    @sowing.setter
    def sowing(self, value):
        sowing = self.management_set.filter(type__code='sowing').last()
        if sowing:
            sowing.date = value
            sowing.save()
        else:
            type = ManagementType.objects.get(code="sowing")
            mgmt = Management(crop=self, date=value, type=type)
            mgmt.save()

    @sowing.deleter
    def sowing(self):
        sowing = self.management_set.filter(type__code='sowing').last()
        if sowing:
            sowing.delete()


    @property
    def harvest(self):
        harvest = self.management_set.filter(type__code='harvest').last()
        if harvest:
            return harvest.date
        else:
            return None

    @harvest.setter
    def harvest(self, value):
        harvest = self.management_set.filter(type__code='harvest').last()
        if harvest:
            harvest.date = value
            harvest.save()
        else:
            type = ManagementType.objects.get(code="harvest")
            mgmt = Management(crop=self, date=value, type=type)
            mgmt.save()

    @harvest.deleter
    def harvest(self):
        harvest = self.management_set.filter(type__code='harvest').last() #type: ignore
        if harvest:
            harvest.delete()

    @property
    def is_current(self):
        if self.harvest and self.harvest > now().date():
            return True
        else:
            return False


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

    crop = models.ForeignKey(Crop, on_delete=models.CASCADE)
