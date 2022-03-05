from django.db import models

class Location(models.Model):
    name = models.CharField(max_length=30)
    latitude = models.FloatField()
    longitude = models.FloatField()

# class Garden(models.Model):
#     name = models.CharField(max_length=30)
    # location = models.ForeignKey(Location, on_delete=models.PROTECT)

class Area(models.Model):
    name = models.CharField(max_length=30)
    # garden = models.ForeignKey(Garden, on_delete=models.PROTECT)
    location = models.ForeignKey(Location, on_delete=models.PROTECT)
    length = models.FloatField()
    width = models.FloatField()
    temp_offset = models.IntegerField()

    @property
    def total_area(self):
        return round(self.length*self.width, 1)

    class Meta:
        ordering = ['name']
