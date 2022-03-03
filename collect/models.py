from django.db import models

from register.models import PlantVariety

class SeedSample(models.Model):
    variety=models.ForeignKey(PlantVariety, on_delete=models.PROTECT)
    notes=models.CharField(max_length=500, help_text="Notes relative to the seed sample")
    growing_season=models.IntegerField(blank=True)

    @property
    def last_germinability(self):
        return str(self.germinability_set.last().value*100) + "%"

    def __str__(self):
        return self.variety.name

class Germinability(models.Model):
    seedsample=models.ForeignKey(SeedSample, on_delete=models.CASCADE)
    value=models.FloatField()
    after_days=models.IntegerField(blank=True, null=True)
    performed_at=models.DateTimeField(blank=True, null=True)

class SampleWeight(models.Model):
    seedsample=models.ForeignKey(SeedSample, on_delete=models.CASCADE)
    value=models.FloatField()
