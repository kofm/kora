from django.db import models
from django.urls import reverse

from frontpage.generic import ModelIsDeletableMixin


class Location(ModelIsDeletableMixin, models.Model):
    name = models.CharField(max_length=30)
    latitude = models.FloatField(blank=True, null=True)
    longitude = models.FloatField(blank=True, null=True)
    order = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("spaces:location_detail", args=[self.pk])

    @classmethod
    def get_create_url(cls):
        return reverse("spaces:location_create")

    def get_update_url(self):
        return reverse("spaces:location_update", args=[self.pk])

    def get_delete_url(self):
        return reverse("spaces:location_delete", args=[self.pk])

    def coordinates(self):
        if self.latitude is not None and self.longitude is not None:
            return f"{self.latitude}° {self.longitude}°"
        return ""
