from django.db import models
from django.urls import reverse
from django.utils.timezone import now

from register.models import PlantVariety
from django.contrib.auth.models import User


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
        return reverse("collect:seedsample-list")

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
    sample_id = models.PositiveIntegerField(unique=True)
    variety = models.ForeignKey(PlantVariety, on_delete=models.PROTECT)
    notes = models.CharField(
        max_length=500,
        help_text="Notes relative to the seed sample",
        blank=True,
        null=True,
        default="",
    )
    growing_season = models.IntegerField(blank=True, null=True)
    position = models.ForeignKey(StoragePosition, on_delete=models.PROTECT)

    class Meta:
        ordering = [
            "-sample_id",
        ]

    def get_absolute_url(self):
        return reverse("collect:seedsample-detail", kwargs={"pk": self.pk})

    @property
    def germinability(self):
        if self.germinability_set.count() > 0:
            return self.germinability_set.last().germinability
        else:
            return None

    @property
    def weight(self):
        if self.sampleweight_set.count() > 0:
            return self.sampleweight_set.last().weight
        else:
            return None

    @property
    def in_cart(self):
        if self.cartitem_set.all():
            return True
        else:
            return False

    def __str__(self):
        return f'#{self.sample_id} - {self.variety.name} ({self.growing_season})'


class Germinability(models.Model):
    seedsample = models.ForeignKey(SeedSample, on_delete=models.CASCADE)
    germinability = models.IntegerField()
    after_days = models.IntegerField(blank=True, null=True)
    performed_at = models.DateField(default=now, blank=True, null=True)

    class Meta:
        ordering = [
            "-performed_at",
        ]

    def __str__(self):
        return str(self.germinability)


class SampleWeight(models.Model):
    seedsample = models.ForeignKey(SeedSample, on_delete=models.CASCADE)
    weight = models.FloatField("sample weight (g)")
    created_at = models.DateField(auto_now_add=True)

    class Meta:
        ordering = [
            "created_at",
        ]


class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateField(auto_now_add=True)

    def __str__(self) -> str:
        return self.user.username


class CartItem(models.Model):
    sample = models.ForeignKey(SeedSample, on_delete=models.CASCADE)
    weight = models.FloatField(
        "quantity retrieved (g)",
        default=0,
    )
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)

    def __str__(self):
        return self.sample.variety.name

    class Meta:
        ordering = ["sample__position"]
