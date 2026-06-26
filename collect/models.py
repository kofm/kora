from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator
from django.db import models, transaction
from django.db.models import Exists, ExpressionWrapper, F, FloatField, OuterRef, Subquery
from django.db.models.aggregates import Coalesce, Count, Max, Sum
from django.db.models.query import Value
from django.db.models.query_utils import Q
from django.forms.widgets import format_html
from django.urls import reverse
from django.utils import timezone

from collect.exceptions import SampleDiscardError
from frontpage.generic import ModelIsDeletableMixin
from frontpage.utils.numbers import format_decimal
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

    @classmethod
    def get_create_url(cls):
        return reverse("collect:storage_create")

    def get_update_url(self):
        return reverse("collect:storage_update", args=(self.pk,))

    def get_delete_url(self):
        return reverse("collect:storage_delete", args=(self.pk,))

    def is_deletable(self):
        return self.stored_positions == 0

    @property
    def cant_delete_msg(self):
        return "You can't delete this storage because it is not empty."

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

    @property
    def highest_stored_position(self):
        return (
            self.storageposition_set.filter(sample__isnull=False)
            .order_by("-name")
            .values_list("name", flat=True)
            .first()
            or 0
        )

    def set_positions(self, value):
        total = self.total_positions
        if value == total:
            return

        with transaction.atomic():
            if value < total:
                highest = self.highest_stored_position
                if value < highest:
                    raise ValueError("Cannot remove positions that contain samples.")

                StoragePosition.objects.filter(storage=self, name__gt=value).delete()
            else:
                StoragePosition.objects.bulk_create(
                    [StoragePosition(storage=self, name=i) for i in range(total + 1, value + 1)],
                    ignore_conflicts=True,
                    batch_size=1000,
                )


class StoragePositionQuerySet(models.QuerySet):
    def empty_positions_for_sample(self, sample_id: int | None = None):
        query = Q(sample__isnull=True)
        if sample_id:
            query |= Q(sample=sample_id)
        return self.filter(query)


class StoragePositionManager(models.Manager):
    def get_queryset(self):
        return StoragePositionQuerySet(self.model, using=self._db).select_related("storage")

    def empty_positions_for_sample(self, *args, **kwargs):
        return self.get_queryset().empty_positions_for_sample(*args, **kwargs)


class StoragePosition(models.Model):
    name = models.PositiveIntegerField()
    storage = models.ForeignKey(Storage, on_delete=models.CASCADE)

    objects = StoragePositionManager()

    def __str__(self):
        return f"{self.storage}-{self.name}"

    def get_absolute_url(self):
        return reverse("collect:storage_detail", args=(self.storage.pk,))


class SampleStatus(models.TextChoices):
    ACTIVE = "A", "Active"
    DISCARDED = "D", "Discarded"


class SampleQueryset(models.QuerySet):
    def active(self):
        return self.filter(status=SampleStatus.ACTIVE)

    def discarded(self):
        return self.filter(status=SampleStatus.DISCARDED)

    def discard(self):
        """Bulk discard.  Samples which are referenced by CartItem
        (thus, are in a Cart) are not updated.
        """
        now = timezone.now()
        return (
            self.active()
            .exclude(cartitem__isnull=False)
            .update(status=SampleStatus.DISCARDED, discarded_at=now, position=None)
        )

    def with_availability(self, excluded_cartitem_pk=None):
        latest_weight_qs = (
            SampleWeight.objects.filter(sample=OuterRef("pk")).order_by("-created_at").values("weight")[:1]
        )

        reserved_filter = Q()
        if excluded_cartitem_pk:
            reserved_filter &= ~Q(cartitem__pk=excluded_cartitem_pk)

        discard_exists_qs = CartItem.objects.filter(
            sample=OuterRef("pk"),
            cart__kind=CartKind.DISCARD,
        )

        qs = self.select_related(
            "variety",
            "variety__species",
            "position",
            "position__storage",
        ).annotate(
            reserved=Coalesce(
                Sum("cartitem__weight", filter=reserved_filter),
                Value(0),
                output_field=FloatField(),
            ),
            last_weight=Coalesce(
                Subquery(
                    latest_weight_qs,
                    output_field=FloatField(),
                ),
                Value(0),
                output_field=FloatField(),
            ),
            available_weight=ExpressionWrapper(
                F("last_weight") - F("reserved"),
                output_field=FloatField(),
            ),
            is_being_discarded=Exists(discard_exists_qs),
        )

        if self.model._meta.ordering:
            qs = qs.order_by(*self.model._meta.ordering)
        return qs

    def detail(self):
        return self.select_related(
            "variety",
            "variety__species",
            "position",
            "position__storage",
        ).prefetch_related("germinability_set", "sampleweight_set")

    def next_id(self):
        current_id = self.aggregate(Max("sample_id", default=1))["sample_id__max"]
        return current_id + 1

    def with_germination(self):
        latest_germinability_qs = (
            Germinability.objects.filter(sample=OuterRef("pk")).order_by("-performed_at").values("germinability")[:1]
        )

        return self.detail().annotate(
            last_germinability=Coalesce(
                Subquery(latest_germinability_qs, output_field=FloatField()),
                Value(0),
                output_field=FloatField(),
            ),
        )


class ActiveSampleManager(models.Manager.from_queryset(SampleQueryset)):  # ty:ignore[unsupported-base]
    """
    Default manager that exposes only active samples.
    """

    def get_queryset(self):
        return super().get_queryset().active()


class Sample(ModelIsDeletableMixin, models.Model):
    sample_id = models.PositiveIntegerField(
        verbose_name="ID",
        help_text="An unique identificative number of the seed sample",
        unique=True,
    )
    variety = models.ForeignKey(PlantVariety, on_delete=models.PROTECT)
    notes = models.CharField(max_length=500, help_text="Notes relative to the seed sample", default="", blank=True)
    growing_season = models.IntegerField(blank=True, null=True)
    position = models.ForeignKey(StoragePosition, on_delete=models.PROTECT, blank=False, null=True)
    status = models.CharField(
        max_length=1,
        choices=SampleStatus.choices,
        default=SampleStatus.ACTIVE,
        db_index=True,
    )
    discarded_at = models.DateTimeField(blank=True, null=True)

    objects = ActiveSampleManager()
    all_objects = SampleQueryset.as_manager()

    class Meta:
        constraints = [
            # - Active samples must have no discarded_at and a storage position
            # - Discarded samples must have discarded_at set and no storage position
            models.CheckConstraint(
                name="sample_status_discarded_at_consistent",
                condition=(
                    (models.Q(status=SampleStatus.ACTIVE) & models.Q(discarded_at__isnull=True))
                    | (models.Q(status=SampleStatus.DISCARDED) & models.Q(discarded_at__isnull=False))
                ),
            ),
            models.CheckConstraint(
                name="sample_status_position_consistent",
                condition=(
                    (models.Q(status=SampleStatus.ACTIVE) & models.Q(position__isnull=False))
                    | (models.Q(status=SampleStatus.DISCARDED) & models.Q(position__isnull=True))
                ),
            ),
        ]
        ordering = ("-sample_id",)

    def __str__(self):
        return f"#{self.sample_id}"

    def get_absolute_url(self):
        return reverse("collect:sample_detail", kwargs={"pk": self.pk})

    def validate_unique(self, exclude=None):
        super().validate_unique(exclude=exclude)

        if exclude and "sample_id" in exclude:
            return

        qs = Sample.all_objects.filter(sample_id=self.sample_id)
        if self.pk:
            qs = qs.exclude(pk=self.pk)
        if qs.exists():
            raise ValidationError({"sample_id": "Sample with this ID already exists."})

    @classmethod
    def get_create_url(cls):
        return reverse("collect:sample_create")

    def get_update_url(self):
        return reverse("collect:sample_update", kwargs={"pk": self.pk})

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
            return format_html(
                '{} g <del class="text-muted"><small>{}</small></del>',
                format_decimal(self.available),
                format_decimal(self.weight),
            )
        elif self.weight:
            return format_html("{} g", format_decimal(self.weight))
        else:
            return "-"

    def get_log(self):
        entries = []
        for germ in self.germinability_set.all():
            entries.append(
                {
                    "type": "germinability",
                    "date": germ.performed_at,
                    "instance": germ,
                }
            )
        for weight in self.sampleweight_set.all():
            entries.append(
                {
                    "type": "weight",
                    "date": weight.created_at,
                    "instance": weight,
                }
            )
        return sorted(entries, key=lambda e: e["date"])

    def discard(self):
        if self.status == SampleStatus.DISCARDED:
            return

        if CartItem.objects.filter(sample=self.pk).exists():
            raise SampleDiscardError("Cannot discard: sample is in a cart.", code="in_cart")

        self.status = SampleStatus.DISCARDED
        self.discarded_at = timezone.now()
        self.position = None
        self.save(update_fields=["status", "discarded_at", "position"])

    def restore(self, position: StoragePosition):
        if self.status == SampleStatus.ACTIVE:
            return

        self.status = SampleStatus.ACTIVE
        self.discarded_at = None
        self.position = position
        self.save(update_fields=["status", "discarded_at", "position"])


class Germinability(models.Model):
    sample = models.ForeignKey(Sample, on_delete=models.CASCADE)
    germinability = models.IntegerField()
    after_days = models.IntegerField(blank=True, null=True)
    performed_at = models.DateTimeField(default=timezone.now, blank=True, null=True)

    class Meta:
        ordering = ("performed_at",)

    def __str__(self):
        return f"{self.germinability}%"

    def get_update_url(self):
        return reverse("collect:germinability_update", args=[self.pk])

    def get_delete_url(self):
        return reverse("collect:germinability_delete", args=[self.pk])


class SampleWeight(models.Model):
    sample = models.ForeignKey(Sample, on_delete=models.CASCADE)
    weight = models.FloatField("sample weight (g)", validators=[MinValueValidator(0.0)])
    created_at = models.DateTimeField("recorded at", default=timezone.now)

    class Meta:
        ordering = ("created_at",)

    def __str__(self):
        return f"{self.weight} g"

    def get_update_url(self):
        return reverse("collect:sampleweight_update", args=(self.pk,))

    def get_delete_url(self):
        return reverse("collect:sampleweight_delete", args=(self.pk,))


class CartQuerySet(models.QuerySet):
    def deactivate_all(self):
        return self.update(is_active=False)


class CartKind(models.TextChoices):
    WITHDRAWAL = "W", "Withdrawal"
    DISCARD = "D", "Discard"


class Cart(models.Model):
    name = models.CharField(help_text="An identificative name for your cart", max_length=100, default="Cart")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="carts")
    is_active = models.BooleanField(default=False)
    created_at = models.DateField(auto_now_add=True)
    default_weight = models.FloatField(help_text="Default quantity to withdraw (g)", default=10)
    kind = models.CharField(max_length=1, choices=CartKind.choices, default=CartKind.WITHDRAWAL, db_index=True)

    objects = CartQuerySet.as_manager()

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=("user",),
                condition=Q(is_active=True),
                name="unique_user_active",
            ),
        ]
        ordering = ("-is_active", "name")

    def __str__(self) -> str:
        return f"{self.name} ({self.get_kind_display()})"

    def get_absolute_url(self):
        return reverse("collect:cart-detail", args=[self.pk])

    def can_withdraw(self):
        return self.kind == CartKind.WITHDRAWAL

    def can_discard(self):
        return self.kind == CartKind.DISCARD

    @transaction.atomic
    def discard(self) -> int:
        if self.kind != CartKind.DISCARD:
            raise ValidationError("Only discard carts can discard samples.")

        cart_sample_ids = list(self.cartitem_set.values_list("sample_id", flat=True))
        if not cart_sample_ids:
            return 0

        blocked_sample_ids = (
            CartItem.objects.filter(sample_id__in=cart_sample_ids)
            .exclude(cart_id=self.pk)
            .values_list("sample_id", flat=True)
        )

        discardable_sample_ids = set(cart_sample_ids) - set(blocked_sample_ids)
        if not discardable_sample_ids:
            return 0

        self.cartitem_set.filter(sample_id__in=discardable_sample_ids).delete()
        return Sample.objects.filter(pk__in=discardable_sample_ids).discard()


class CartItem(models.Model):
    sample = models.ForeignKey(Sample, on_delete=models.PROTECT)
    weight = models.FloatField("quantity retrieved (g)", default=None, blank=True, null=True)
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ("sample__position",)
        constraints = [models.UniqueConstraint(fields=("cart", "sample"), name="uniq_cart_sample")]

    def __str__(self):
        return f"{self.weight} g of Sample #{self.sample.sample_id}"

    def save(self, *args, **kwargs):
        self.full_clean()
        return super().save(*args, **kwargs)

    def clean(self):
        super().clean()

        if self.cart.kind == CartKind.DISCARD:
            if self.weight is not None:
                raise ValidationError({"weight": "Discard carts do not use quantities."})
            return

        sample = Sample.objects.with_availability(excluded_cartitem_pk=self.pk).get(pk=self.sample_id)
        if not sample:
            raise ValidationError({"sample": "Selected sample does not exist."})

        if self.weight > sample.available:
            raise ValidationError(
                {"weight": (f"Cannot reserve {self.weight:g} g; only {sample.available:g} g available.")}
            )

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
