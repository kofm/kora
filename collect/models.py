from django.db import models

from register.models import PlantVariety


class Storage(models.Model):
    """
    This is a container of multiple seed samples. The number of slots available
    for seed samples is defined by how many StoragePositions are associated with
    each instance. They should be ideally ordered by name.
    """

    name = models.CharField(max_length=200)

    class Meta:
        ordering = ["name"]

    def __str__(self) -> str:
        return self.name


class StoragePosition(models.Model):
    name = models.CharField(max_length=200)
    storage = models.ForeignKey(Storage, on_delete=models.PROTECT)

    def __str__(self) -> str:
        return self.storage.name + "-" + self.name


class SeedSample(models.Model):
    variety = models.ForeignKey(PlantVariety, on_delete=models.PROTECT)
    notes = models.CharField(
        max_length=500, help_text="Notes relative to the seed sample"
    )
    growing_season = models.IntegerField(blank=True)
    position = models.ForeignKey(
        StoragePosition, blank=True, null=True, on_delete=models.PROTECT
    )

    @property
    def last_germinability(self):
        if self.germinability_set.count() > 0:
            return str(self.germinability_set.last().value * 100) + "%"
        else:
            return ""

    def __str__(self):
        return self.variety.name


class Germinability(models.Model):
    seedsample = models.ForeignKey(SeedSample, on_delete=models.CASCADE)
    value = models.FloatField()
    after_days = models.IntegerField(blank=True, null=True)
    performed_at = models.DateTimeField(blank=True, null=True)


class SampleWeight(models.Model):
    seedsample = models.ForeignKey(SeedSample, on_delete=models.CASCADE)
    value = models.FloatField()
