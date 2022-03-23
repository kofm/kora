from django.db import models
from django.urls import reverse

from register.models import PlantVariety


class Storage(models.Model):
    """
    This is a container of multiple seed samples. The number of slots available
    for seed samples is defined by how many StoragePositions are associated with
    each instance. They should be ideally ordered by name.
    """

    name = models.CharField(max_length=200, unique=True)

    class Meta:
        ordering = ["name"]

    def __str__(self) -> str:
        return self.name

    def get_absolute_url(self):
        return reverse('collect:seedsamples-list')

    @property
    def available_positions(self):
        return self.storageposition_set.filter(seedsample__isnull=True).count()

    @property
    def stored_samples(self):
        return self.storageposition_set.filter(seedsample__isnull=False).count()

class StoragePosition(models.Model):
    name = models.CharField(max_length=200)
    storage = models.ForeignKey(Storage, on_delete=models.PROTECT)

    def __str__(self) -> str:
        return self.storage.name + "-" + self.name


class SeedSample(models.Model):
    variety = models.ForeignKey(PlantVariety, on_delete=models.PROTECT)
    notes = models.CharField(
        max_length=500, help_text="Notes relative to the seed sample", blank=True, null=True
    )
    growing_season = models.IntegerField(blank=True)
    position = models.ForeignKey(
        StoragePosition, blank=True, null=True, on_delete=models.PROTECT
    )

    def get_absolute_url(self):
        return reverse('collect:seedsample-detail', kwargs={'pk' : self.pk})

    @property
    def last_germinability(self):
        if self.germinability_set.count() > 0:
            return str(self.germinability_set.last().value) + "%"
        else:
            return ""

    def __str__(self):
        if self.variety.names.last():
            return self.variety.names.last()
        else:
            return ''


class Germinability(models.Model):
    seedsample = models.ForeignKey(SeedSample, on_delete=models.CASCADE)
    value = models.IntegerField()
    after_days = models.IntegerField(blank=True, null=True)
    performed_at = models.DateField(blank=True, null=True)

    class Meta:
        ordering = [
            "performed_at",
        ]

    @property
    def value_percent(self):
        return self.value * 100


class SampleWeight(models.Model):
    seedsample = models.ForeignKey(SeedSample, on_delete=models.CASCADE)
    value = models.FloatField()
    created_at = models.DateField(auto_now_add=True)

    class Meta:
        ordering = [
            "created_at",
        ]
