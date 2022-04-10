from django.db import models
from django.utils.timezone import now

class Location(models.Model):
    name = models.CharField(max_length=30)
    latitude = models.FloatField()
    longitude = models.FloatField()

    def __str__(self):
        return self.name

class Area(models.Model):
    name = models.CharField(max_length=30)
    location = models.ForeignKey(Location, on_delete=models.PROTECT)
    length = models.FloatField()
    width = models.FloatField()
    temp_offset = models.IntegerField()

    @property
    def total_area(self):
        return round(self.length*self.width, 1)

    def current_crops(self):
        return self.crop_set.filter(management__type__code='harvest', management__date__gt=now().date()).distinct()

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']
