from django.db import models
from register.models import PlantVariety

class Protocol(models.Model):
    name = models.CharField(max_length=200)

class Description(models.Model):
    name = models.CharField(max_length=200)
    protocol = models.ForeignKey(Protocol,
            on_delete=models.PROTECT)
    variety = models.ForeignKey(PlantVariety, on_delete=models.RESTRICT,
            related_name= 'variety')

class Trait(models.Model):
    numeric_id = models.IntegerField()
    description = models.CharField(max_length=200)
    protocol = models.ForeignKey(Protocol, on_delete=models.PROTECT)

class State(models.Model):
    numeric_id = models.IntegerField()
    description = models.CharField(max_length=200)
    trait = models.ForeignKey(Trait, models.PROTECT)

class Expression(models.Model):
    recording_date = models.DateField()
    georeference_lat = models.FloatField()
    georeference_lon = models.FloatField()
    state_of_expression = models.ForeignKey(State, on_delete=models.PROTECT)
    description = models.ForeignKey(Description, on_delete=models.RESTRICT)
