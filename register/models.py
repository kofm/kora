from datetime import date
from enum import unique

from django.db import models
from django.utils.functional import cached_property

class PlantSpecies(models.Model):
    common_name = models.CharField(max_length=100, unique=True)
    latin_name = models.CharField(max_length=100)
    plant_types = (
        ("tree", "Tree"),
        ("shrub", "Shrub"),
        ("vegetable", "Vegetable"),
        ("herbaceous", "Herbaceous"),
    )
    plant_type = models.CharField(max_length=100, choices=plant_types)

    @property
    def total_descriptions(self):
        return self.variety.filter(description__isnull=False).count()

    @property
    def total_seedsamples(self):
        return self.variety.filter(seedsample__isnull=False).count()

    def __str__(self):
        return self.common_name

    class Meta:
        ordering = ["common_name"]

class PlantVariety(models.Model):
    species = models.ForeignKey(
        PlantSpecies, on_delete=models.CASCADE, related_name="variety"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["names__name"]

    @cached_property
    def name(self):
        if self.names.count() > 0:
            return self.names.order_by('-change_date').first().name
        else:
            return ''


    def __str__(self):
        return self.name

class PlantVarietyName(models.Model):
    name = models.CharField(max_length=200)
    variety = models.ForeignKey(PlantVariety, on_delete=models.CASCADE, related_name="names")
    change_date = models.DateField(blank=True, null=True, default=date.today)
