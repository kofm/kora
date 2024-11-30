import datetime

from django.contrib.auth.models import User
from django.db import models, transaction
from django.db.models.constraints import UniqueConstraint
from django.db.models.query_utils import Q
from django.urls import reverse
from django.utils.timezone import now
from frontpage.generic import ModelIsDeletableMixin
from register.models import PlantVariety


class Storage(models.Model):
    """Container of multiple seed samples.

    The number of slots available for seed samples is defined by how
    many StoragePositions are associated with each instance.
    """

    name = models.CharField(max_length=200, unique=True)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ("name",)
        verbose_name_plural = "Storage"

    def __str__(self) -> str:
        return self.name

    def get_absolute_url(self):
        return reverse("collect:storage_detail", args=(self.pk,))

    def get_update_url(self):
        return reverse("collect:storage_update", args=(self.pk,))

    def get_delete_url(self):
        return reverse("collect:storage_delete", args=(self.pk,))

    def is_deletable(self):
        return self.stored_samples == 0

    def increase_positions(self, value):
        if value <= self.total_positions:
            return
        with transaction.atomic():
            for i in range(self.total_positions + 1, value + 1):
                StoragePosition.objects.get_or_create(storage=self, name=str(i))

    def decrease_positions(self, value):
        if value >= self.total_positions:
            return
        positions = [str(i) for i in range(value + 1, self.total_positions + 1)]
        StoragePosition.objects.filter(storage=self, name__in=positions).delete()

    @property
    def total_positions(self):
        return self.storageposition_set.count()

    @property
    def available_positions(self):
        return self.storageposition_set.filter(seedsample__isnull=True).count()

    @property
    def stored_samples(self):
        return self.storageposition_set.filter(seedsample__isnull=False).count()


class StoragePosition(models.Model):
    name = models.CharField(max_length=200)
    storage = models.ForeignKey(Storage, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return f"{self.storage.name}-{self.name}"

    def get_absolute_url(self):
        return reverse("collect:storage_detail", args=(self.storage.pk,))


class SeedSample(ModelIsDeletableMixin, models.Model):
    sample_id = models.PositiveIntegerField(
        verbose_name="ID", help_text="An unique identificative number of the seed sample", unique=True
    )
    variety = models.ForeignKey(PlantVariety, on_delete=models.PROTECT)
    notes = models.CharField(max_length=500, help_text="Notes relative to the seed sample", default="")
    growing_season = models.IntegerField(blank=True, null=True)
    position = models.ForeignKey(StoragePosition, on_delete=models.PROTECT)

    class Meta:
        ordering = ("-sample_id",)

    def __str__(self):
        return f"#{self.sample_id}"

    def get_absolute_url(self):
        return reverse("collect:seedsample_detail", kwargs={"pk": self.pk})

    def get_delete_url(self):
        return reverse("collect:seedsample_delete", kwargs={"pk": self.pk})

    @property
    def growing_season_as_date(self):
        now = datetime.datetime.now()
        return datetime.datetime(self.growing_season, now.month, now.day)

    @property
    def germinability(self):
        if self.germinability_set.count() > 0:
            return self.germinability_set.last().germinability
        return None

    @property
    def weight(self):
        if self.sampleweight_set.count() > 0:
            return self.sampleweight_set.last().weight
        return None

    @property
    def duplicate_samples(self):
        return SeedSample.objects.filter(variety=self.variety).exclude(pk=self.pk)


class Germinability(models.Model):
    seedsample = models.ForeignKey(SeedSample, on_delete=models.CASCADE)
    germinability = models.IntegerField()
    after_days = models.IntegerField(blank=True, null=True)
    performed_at = models.DateField(default=now, blank=True, null=True)

    class Meta:
        ordering = ("-performed_at",)

    def __str__(self):
        return str(self.germinability)


class SampleWeight(models.Model):
    seedsample = models.ForeignKey(SeedSample, on_delete=models.CASCADE)
    weight = models.FloatField("sample weight (g)")
    created_at = models.DateField(auto_now_add=True)

    class Meta:
        ordering = ("created_at",)

    def __str__(self):
        return f"{self.seedsample} ({self.created_at}): {self.weight}g"


class CartManager(models.Manager):
    def active(self):
        return self.filter(active=True).last()


class Cart(models.Model):
    name = models.CharField(help_text="An identificative name for your cart", max_length=100, default="Cart")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="carts")
    active = models.BooleanField(default=False)
    created_at = models.DateField(auto_now_add=True)

    objects = CartManager()

    def __str__(self) -> str:
        return self.name

    class Meta:
        constraints = [
            UniqueConstraint(
                fields=[
                    "user",
                ],
                condition=Q(active=True),
                name="unique_user_active",
            )
        ]
        ordering = ["-active", "name"]

    def get_absolute_url(self):
        return reverse("collect:cart-detail", args=[self.pk])


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
