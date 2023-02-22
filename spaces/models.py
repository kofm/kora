from django.db import models
from django.utils.timezone import now


class Location(models.Model):
    name = models.CharField(max_length=30)
    latitude = models.FloatField(blank=True, null=True)
    longitude = models.FloatField(blank=True, null=True)

    def __str__(self):
        return self.name


class Area(models.Model):
    name = models.CharField(max_length=30)
    location = models.ForeignKey(Location, on_delete=models.CASCADE)
    length = models.FloatField(help_text="The length of the area, in meters.")
    width = models.FloatField(help_text="The width of the area, in meters.")
    order = models.PositiveIntegerField(help_text="The ordering of the area within its location")

    @property
    def total_area(self):
        return round(self.length * self.width, 1)

    def current_crops(self):
        return self.crop_set.filter(
            management__type__code="sowing", management__date__lt=now().date()
        ).distinct()

    def __str__(self):
        return self.name

    class Meta:
        ordering = ["order", "name"]
