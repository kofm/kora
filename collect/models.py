from django.contrib.auth.models import User
from django.core.validators import MinValueValidator
from django.db import models, transaction
from django.db.models import F, IntegerField, RowRange, Window
from django.db.models.aggregates import Max
from django.db.models.functions import Concat, LastValue
from django.db.models.query import Cast, Value
from django.db.models.query_utils import Q
from django.urls import reverse
from django.utils import timezone

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
        return self.storageposition_set.filter(sample__isnull=True).count()

    @property
    def stored_samples(self):
        return self.storageposition_set.filter(sample__isnull=False).count()


class StoragePositionQuerySet(models.QuerySet):
    def empty_positions_for_accession(self, sample_id: int | None = None):
        query = Q(sample__isnull=True)
        if sample_id:
            query |= Q(sample=sample_id)
        return self.filter(query)

    def position_values_list(self):
        qs = self.select_related("storage").annotate(
            position_name=Concat("storage__name", Value("-"), "name"),
            posn=Cast("name", output_field=IntegerField()),
        )
        qs = qs.order_by("storage__name", "posn")
        return qs.values_list("pk", "position_name")


class StoragePositionManager(models.Manager):
    def get_queryset(self):
        return StoragePositionQuerySet(self.model, using=self._db).select_related("storage")

    def empty_positions_for_accession(self, *args, **kwargs):
        return self.get_queryset().empty_positions_for_accession(*args, **kwargs)


class StoragePosition(models.Model):
    name = models.CharField(max_length=200)
    storage = models.ForeignKey(Storage, on_delete=models.CASCADE)

    objects = StoragePositionManager()

    def __str__(self):
        return f"{self.storage}-{self.name}"

    def get_absolute_url(self):
        return reverse("collect:storage_detail", args=(self.storage.pk,))


class SampleQueryset(models.QuerySet):
    def with_weight(self):
        return (
            self.select_related("variety", "variety__species", "position", "position__storage")
            .annotate(
                last_weight=Window(
                    expression=LastValue("sampleweight__weight"),
                    partition_by=F("id"),
                    order_by=F("sampleweight__created_at").asc(),
                    frame=RowRange(start=None, end=None),
                ),
            )
            .distinct()
        )

    def detail(self):
        return self.select_related("variety", "variety__species", "position", "position__storage").prefetch_related(
            "germinability_set", "sampleweight_set"
        )

    def next_id(self):
        qs = self.aggregate(Max("sample_id", default=1))
        return qs["sample_id__max"] + 1

    def with_germination(self):
        return (
            self.select_related("variety", "variety__species", "position", "position__storage")
            .annotate(
                last_germinability=Window(
                    expression=LastValue("germinability__germinability"),
                    partition_by=F("id"),
                    order_by=F("germinability__performed_at").asc(),
                    frame=RowRange(start=None, end=None),
                ),
            )
            .distinct()
        )


class Sample(ModelIsDeletableMixin, models.Model):
    sample_id = models.PositiveIntegerField(
        verbose_name="ID", help_text="An unique identificative number of the seed sample", unique=True
    )
    variety = models.ForeignKey(PlantVariety, on_delete=models.PROTECT)
    notes = models.CharField(max_length=500, help_text="Notes relative to the seed sample", default="", blank=True)
    growing_season = models.IntegerField(blank=True, null=True)
    position = models.ForeignKey(StoragePosition, on_delete=models.PROTECT)

    objects = SampleQueryset.as_manager()

    class Meta:
        ordering = ("-sample_id",)

    def __str__(self):
        return f"#{self.sample_id}"

    def get_absolute_url(self):
        return reverse("collect:sample_detail", kwargs={"pk": self.pk})

    def get_delete_url(self):
        return reverse("collect:sample_delete", kwargs={"pk": self.pk})

    @property
    def germinability(self):
        if self.germinability_set.count() > 0:
            return self.germinability_set.last().germinability
        return None

    @property
    def weight(self):
        sampleweight = self.sampleweight_set.last()
        if sampleweight:
            return sampleweight.weight
        return None

    def last_sampleweight(self):
        return self.sampleweight_set.last()

    @property
    def duplicate_samples(self):
        return Sample.objects.with_weight().with_germination().filter(variety=self.variety).exclude(pk=self.pk)

    def get_log(self):
        germ_rates = self.germinability_set.all()
        weights = self.sampleweight_set.all()

        log = []

        for germ in germ_rates:
            log.append(
                {
                    "pk": self.pk,
                    "date": germ.performed_at,
                    "germinability": germ.germinability,
                    "update_url": germ.get_update_url(),
                    "delete_url": germ.get_delete_url(),
                }
            )

        for weight in weights:
            log.append(
                {
                    "pk": self.pk,
                    "date": weight.created_at,
                    "weight": weight.weight,
                    "update_url": weight.get_update_url(),
                    "delete_url": weight.get_delete_url(),
                }
            )

        return sorted(log, key=lambda e: e["date"])


class Germinability(models.Model):
    sample = models.ForeignKey(Sample, on_delete=models.CASCADE)
    germinability = models.IntegerField()
    after_days = models.IntegerField(blank=True, null=True)
    performed_at = models.DateField(default=timezone.localdate, blank=True, null=True)

    class Meta:
        ordering = ("performed_at",)

    def __str__(self):
        return str(self.germinability)

    def get_update_url(self):
        return reverse("collect:germinability_update", args=[self.pk])

    def get_delete_url(self):
        return reverse("collect:germinability_delete", args=[self.pk])


class SampleWeight(models.Model):
    sample = models.ForeignKey(Sample, on_delete=models.CASCADE)
    weight = models.FloatField("sample weight (g)", validators=[MinValueValidator(0.0)])
    created_at = models.DateField(default=timezone.localdate)

    class Meta:
        ordering = ("created_at",)

    def __str__(self):
        return f"{self.weight}g"

    def get_update_url(self):
        return reverse("collect:sampleweight_update", args=(self.pk,))

    def get_delete_url(self):
        return reverse("collect:sampleweight_delete", args=(self.pk,))


class CartQuerySet(models.QuerySet):
    def deactivate_all(self):
        return self.update(is_active=False)


class Cart(models.Model):
    name = models.CharField(help_text="An identificative name for your cart", max_length=100, default="Cart")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="carts")
    is_active = models.BooleanField(default=False)
    created_at = models.DateField(auto_now_add=True)
    default_weight = models.FloatField(help_text="Default quantity to retrieve (g)", default=10)

    objects = CartQuerySet.as_manager()

    class Meta:
        constraints = (
            models.UniqueConstraint(
                fields=("user",),
                condition=Q(is_active=True),
                name="unique_user_active",
            ),
        )
        ordering = ("-is_active", "name")

    def __str__(self) -> str:
        return self.name

    def get_absolute_url(self):
        return reverse("collect:cart-detail", args=[self.pk])


class CartItem(models.Model):
    sample = models.ForeignKey(Sample, on_delete=models.PROTECT)
    weight = models.FloatField("quantity retrieved (g)", default=0)
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ("sample__position",)

    def __str__(self):
        return self.sample.variety.name
