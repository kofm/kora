from django.db import models

class Garden(models.Model):
    name = models.CharField(max_length=30)

class Area(models.Model):
    name = models.CharField(max_length=30)
    garden = models.ForeignKey(Garden, on_delete=models.PROTECT)
    length = models.FloatField()
    width = models.FloatField()
    temp_offset = models.IntegerField()
