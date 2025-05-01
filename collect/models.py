from django.contrib.auth.models import User
from django.core.validators import MinValueValidator
from django.db import models, transaction
from django.db.models import ExpressionWrapper, F, FloatField, IntegerField, OuterRef, Subquery
from django.db.models.aggregates import Coalesce, Count, Max, Sum
from django.db.models.functions import Concat
from django.db.models.query import Cast, Value
from django.db.models.query_utils import Q
from django.forms import ValidationError
from django.forms.widgets import format_html
from django.urls import reverse
from django.utils import timezone

from frontpage.generic import ModelIsDeletableMixin
from register.models import PlantVariety


class StorageQuerySet(models.QuerySet):
    def with_position_counts(self):
        return self.annotate(
            total_positions_count=Count("storageposition", distinct=True),
            stored_positions_count=Count(
                "storageposition", filter=Q(storageposition__sample__isnull=False), distinct=True
            ),
            available_positions_count=Count(
                "storageposition", filter=Q(storageposition__sample__isnull=True), distinct=True
            ),
        )


class StorageManager(models.Manager):
    def get_queryset(self):
        return StorageQuerySet(self.model, using=self._db)

    def with_position_counts(self):
        return self.get_queryset().with_position_counts()


class Storage(models.Model):
    """Container of multiple seed samples.

    The number of slots available for seed samples is defined by how
    many StoragePositions are associated with each instance.
    """

    name = models.CharField(max_length=200, unique=True)
    order = models.PositiveIntegerField(default=0)

    objects = StorageManager()

    class Meta:
        ordering = ("name",)
        verbose_name_plural = "storage"

    def __str__(self) -> str:
        return self.name

    def get_absolute_url(self):
        return reverse("collect:storage_detail", args=(self.pk,))

    def get_update_url(self):
        return reverse("collect:storage_update", args=(self.pk,))

    def get_delete_url(self):
        return reverse("collect:storage_delete", args=(self.pk,))

    def is_deletable(self):
        return self.stored_positions == 0

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
        if hasattr(self, "total_positions_count"):
            return self.total_positions_count
        return self.storageposition_set.count()

    @property
    def stored_positions(self):
        if hasattr(self, "stored_positions_count"):
            return self.stored_positions_count
        return self.storageposition_set.filter(sample__isnull=False).count()

    @property
    def available_positions(self):
        if hasattr(self, "available_positions_count"):
            return self.available_positions_count
        return self.storageposition_set.filter(sample__isnull=True).count()


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
    def with_availability(self, excluded_cartitem_pk=None):
        latest_weight_sq = (
            SampleWeight.objects.filter(sample=OuterRef("pk")).order_by("-created_at").values("weight")[:1]
        )

        reserved_filter = Q()
        if excluded_cartitem_pk:
            reserved_filter &= ~Q(cartitem__pk=excluded_cartitem_pk)

        qs = self.select_related("variety", "variety__species", "position", "position__storage").annotate(
            reserved=Coalesce(
                Sum("cartitem__weight", filter=reserved_filter),
                Value(0),
                output_field=FloatField(),
            ),
            last_weight=Coalesce(
                Subquery(latest_weight_sq, output_field=FloatField()),
                Value(0),
                output_field=FloatField(),
            ),
            available_weight=ExpressionWrapper(
                F("last_weight") - F("reserved"),
                output_field=FloatField(),
            ),
        )

        if self.model._meta.ordering:
            qs = qs.order_by(*self.model._meta.ordering)
        return qs

    def detail(self):
        return self.select_related("variety", "variety__species", "position", "position__storage").prefetch_related(
            "germinability_set", "sampleweight_set"
        )

    def next_id(self):
        qs = self.aggregate(Max("sample_id", default=1))
        return qs["sample_id__max"] + 1

    def with_germination(self):
        latest_germinability_sq = (
            Germinability.objects.filter(sample=OuterRef("pk")).order_by("-performed_at").values("germinability")[:1]
        )

        return self.detail().annotate(
            last_germinability=Coalesce(
                Subquery(latest_germinability_sq, output_field=FloatField()),
                Value(0),
                output_field=FloatField(),
            ),
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
        if hasattr(self, "last_germinability"):
            return self.last_germinability
        if self.germinability_set.count() > 0:
            return self.germinability_set.last().germinability
        return None

    @property
    def weight(self):
        if hasattr(self, "last_weight"):
            return self.last_weight
        sampleweight = self.sampleweight_set.last()
        if sampleweight:
            return sampleweight.weight
        return None

    @property
    def duplicate_samples(self):
        return Sample.objects.with_availability().filter(variety=self.variety).exclude(pk=self.pk)

    @property
    def available(self):
        # Fetch using .with_availability()
        aw = getattr(self, "available_weight", None)
        if aw is None:
            last = self.sampleweight_set.values_list("weight", flat=True).last() or 0
            reserved = self.cartitem_set.aggregate(total=Coalesce(Sum("weight"), Value(0), output_field=FloatField()))
            aw = last - reserved["total"]
        return aw if aw > 0 else 0

    def get_weight_display(self):
        if self.weight and self.weight > self.available:
            return format_html('{} g <del class="text-muted"><small>{}</small></del>', self.available, self.weight)
        elif self.weight:
            return format_html("{} g", self.weight)
        else:
            return "-"

    def get_log(self):
        entries = []
        for germ in Germinability.objects.filter(sample_id=self.pk):
            entries.append(
                {
                    "pk": self.pk,
                    "date": germ.performed_at,
                    "germinability": germ.germinability,
                    "update_url": germ.get_update_url(),
                    "delete_url": germ.get_delete_url(),
                }
            )
        for weight in SampleWeight.objects.filter(sample_id=self.pk):
            entries.append(
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
        return f"{self.weight} g of Sample #{self.sample.sample_id}"

    def clean(self):
        super().clean()

        sample = Sample.objects.with_availability(excluded_cartitem_pk=self.pk).get(pk=self.sample_id)
        if not sample:
            raise ValidationError({"sample": "Selected sample does not exist."})

        if self.weight > sample.available:
            raise ValidationError(
                {"weight": (f"Cannot reserve {self.weight:g} g; only {sample.available:g} g available.")}
            )

    def save(self, *args, **kwargs):
        self.full_clean()
        return super().save(*args, **kwargs)

    def create_sampleweight(self):
        """
        Returns a new (unsaved) SampleWeight that reflects
        withdrawing this CartItem’s `weight` from the sample.
        """
        last_sw = self.sample.sampleweight_set.order_by("-created_at").first()
        last_weight = last_sw.weight if last_sw else 0.0

        new_weight = last_weight - self.weight
        if new_weight < 0:
            raise ValidationError(f"Cannot retrieve {self.weight:g}g: only {last_weight:g}g in stock.")

        return SampleWeight(sample=self.sample, weight=new_weight)
