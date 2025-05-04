from django.db import models
from django.urls import reverse
from django.utils.timezone import now

from frontpage.generic import ModelIsDeletableMixin


class Location(models.Model):
    name = models.CharField(max_length=30)
    order = models.PositiveIntegerField(default=0)
    latitude = models.FloatField(blank=True, null=True)
    longitude = models.FloatField(blank=True, null=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("spaces:location-detail", args=[self.pk])

    def get_update_url(self):
        return reverse("spaces:location-update", args=[self.pk])

    def get_delete_url(self):
        return reverse("spaces:location-delete", args=[self.pk])


class Area(ModelIsDeletableMixin, models.Model):
    name = models.CharField(max_length=30, help_text="The identificative name of the area")
    location = models.ForeignKey(Location, on_delete=models.CASCADE)
    length = models.FloatField(help_text="The length of the area, in meters")
    width = models.FloatField(help_text="The width of the area, in meters")
    order = models.PositiveIntegerField(help_text="The ordering of the area within its location", default=0)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ["order", "name"]

    def get_absolute_url(self):
        return reverse("spaces:area-detail", args=(self.pk,))

    def get_update_url(self):
        return reverse("spaces:area-update", args=(self.pk,))

    def get_delete_url(self):
        return reverse("spaces:area-delete", args=(self.pk,))

    @property
    def total_area(self):
        return round(self.length * self.width, 1)

    def current_crops(self):
        return self.crop_set.filter(management__type__code="sowing", management__date__lt=now().date()).distinct()
