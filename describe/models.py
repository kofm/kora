from django.db import models
from register.models import PlantVariety,PlantSpecies

class Protocol(models.Model):
    name = models.CharField(max_length=200)
    specie = models.ForeignKey(PlantSpecies, on_delete=models.PROTECT)

    def __str__(self):
        return self.name

class Description(models.Model):
    name = models.CharField(max_length=200)
    protocol = models.ForeignKey(Protocol,
            on_delete=models.PROTECT)
    variety = models.ForeignKey(PlantVariety, on_delete=models.RESTRICT)

    def __str__(self):
        return str(self.variety) + ' (' + self.name + ')'

class Trait(models.Model):
    numeric_id = models.IntegerField(null=True, blank=True)
    description = models.CharField(max_length=200)
    protocol = models.ForeignKey(Protocol, on_delete=models.PROTECT,
            null = True, blank=True)

    def __str__(self):
        return str(self.numeric_id) + '. ' + self.description

class State(models.Model):
    numeric_id = models.IntegerField()
    description = models.CharField(max_length=200)
    trait = models.ForeignKey(Trait, models.PROTECT)

    def __str__(self):
        return str(self.numeric_id) + '. ' + self.description

class Expression(models.Model):
    recording_date = models.DateField()
    georeference_lat = models.FloatField()
    georeference_lon = models.FloatField()
    state_of_expression = models.ForeignKey(State, on_delete=models.PROTECT)
    description = models.ForeignKey(Description, on_delete=models.RESTRICT)

    def __str__(self):
        return str(self.state_of_expression) + " (" + str(self.recording_date) + ")"

class Measure(models.Model):
    linked_trait = models.ForeignKey(Trait, on_delete=models.PROTECT)
    georeference_lat = models.FloatField()
    georeference_lon = models.FloatField()
    measure_unit = models.CharField(max_length=50)
    value = models.FloatField()
