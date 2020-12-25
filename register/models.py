from enum import unique
from django.db import models

class PlantSpecies(models.Model):
    common_name = models.CharField(max_length=100,unique=True)
    latin_name = models.CharField(max_length=100)
    plant_types = (
            ('tree', 'Tree'),
            ('shrub', 'Shrub'),
            ('vegetable', 'Vegetable'),
            ('herbaceous', 'Herbaceous')
            )
    plant_type = models.CharField(max_length=100, choices=plant_types)

    def __str__(self):
        return self.common_name

    class Meta:
        ordering = ["common_name"]


class PlantVariety(models.Model):
    name = models.CharField(max_length=100)
    species = models.ForeignKey(PlantSpecies,
            on_delete=models.CASCADE,
            related_name='variety')

    class Meta:
        constraints = [
                models.UniqueConstraint(
                    fields = ['species', 'name'],
                    name = 'unique name'
                    )
                ]

    def __str__(self):
        return self.name
