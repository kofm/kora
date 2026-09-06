"""Crop layouts, crops, field books, targets, and observations."""

from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import models
from django.urls import reverse
from django.utils import timezone
from django.utils.functional import cached_property
from django.utils.timezone import now

from describe.models import State, Trait
from frontpage.generic import ModelIsDeletableMixin
from parameters.models import Parameter, ParameterValue
from register.models import PlantVariety
from spaces.models import Location


class CropLayoutQuerySet(models.QuerySet):
    def visible(self):
        return self.filter(archived_at__isnull=True)

    def archived(self):
        return self.filter(archived_at__isnull=False)


class CropLayout(ModelIsDeletableMixin, models.Model):
    cant_delete_msg = "Remove all crops and field books before deleting this crop layout."

    name = models.CharField(max_length=100, help_text="A descriptive name for the layout")
    location = models.ForeignKey(
        Location,
        on_delete=models.PROTECT,
        related_name="crop_layouts",
        help_text="The location to which the layout belongs",
    )
    description = models.TextField(blank=True, default="", help_text="Additional information about the layout")
    ncol = models.PositiveIntegerField(
        "Columns", default=1, help_text="The number of columns in which crops are arranged"
    )
    archived_at = models.DateTimeField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = CropLayoutQuerySet.as_manager()

    class Meta:
        ordering = ("name", "pk")
        constraints = [models.CheckConstraint(condition=models.Q(ncol__gt=0), name="crop_layout_ncol_positive")]

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("calculator:layout_detail", args=(self.pk,))

    @classmethod
    def get_create_url(cls):
        return reverse("calculator:layout_create")

    def get_update_url(self):
        return reverse("calculator:layout_update", args=(self.pk,))

    @property
    def is_archived(self):
        return self.archived_at is not None

    def get_archive_url(self):
        return reverse("calculator:layout_archive", args=(self.pk,))

    def get_restore_url(self):
        return reverse("calculator:layout_restore", args=(self.pk,))

    def archive(self):
        if self.archived_at is None:
            self.archived_at = timezone.now()
            self.save(update_fields=["archived_at", "updated_at"])

    def restore(self):
        if self.archived_at is not None:
            self.archived_at = None
            self.save(update_fields=["archived_at", "updated_at"])


class CropQuerySet(models.QuerySet):
    def mutable(self):
        return self.filter(layout__archived_at__isnull=True)


class Crop(ModelIsDeletableMixin, models.Model):
    layout = models.ForeignKey(CropLayout, on_delete=models.PROTECT, related_name="crops")
    variety = models.ForeignKey(PlantVariety, on_delete=models.PROTECT)
    order = models.PositiveIntegerField(default=0)
    notes = models.CharField(max_length=500, help_text="Notes relative to the Crop", blank=True, default="")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = CropQuerySet.as_manager()

    class Meta:
        ordering = ("order", "pk")

    def __str__(self):
        return f"Crop #{self.pk}"

    def get_absolute_url(self):
        return reverse("calculator:crop_detail", args=(self.pk,))

    def get_update_url(self):
        return reverse("calculator:crop_update", args=(self.pk,))

    def get_delete_url(self):
        return reverse("calculator:crop_delete", args=(self.pk,))


class CropParameter(ParameterValue):
    crop = models.ForeignKey(Crop, on_delete=models.CASCADE, related_name="parameters")

    class Meta:
        ordering = ["parameter__code"]


class ManagementType(ModelIsDeletableMixin, models.Model):
    cant_delete_msg = "This management operation cannot be deleted because it is in use."

    code = models.CharField(max_length=30)
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, default="")

    class Meta:
        ordering = ("name", "pk")
        verbose_name_plural = "management operations"

    def __str__(self):
        return self.name

    @classmethod
    def get_create_url(cls):
        return reverse("calculator:managementtype_create")

    def get_update_url(self):
        return reverse("calculator:managementtype_update", args=(self.pk,))

    def get_delete_url(self):
        return reverse("calculator:managementtype_delete", args=(self.pk,))


class Management(models.Model):
    type = models.ForeignKey(ManagementType, on_delete=models.PROTECT)
    date = models.DateField()
    layout = models.ForeignKey(CropLayout, on_delete=models.CASCADE, related_name="managements")
    notes = models.TextField(blank=True, default="")

    def __str__(self) -> str:
        return str(self.date) + " - " + self.type.name


class FieldBookQuerySet(models.QuerySet):
    def mutable(self):
        return self.filter(layout__archived_at__isnull=True)

    def with_progress_data(self):
        return self.prefetch_related(
            models.Prefetch(
                "steps",
                queryset=Step.objects.prefetch_related(
                    "traittarget",
                    "parametertarget",
                    "traitobservation__state",
                    "parameterobservation",
                ),
                to_attr="steps_for_progress",
            )
        )


class FieldBook(ModelIsDeletableMixin, models.Model):
    cant_delete_msg = "You can't remove this FieldBook because there are planned observations."

    name = models.CharField(max_length=200)
    layout = models.ForeignKey(CropLayout, on_delete=models.PROTECT, related_name="fieldbooks")
    display_config = models.JSONField(null=True)

    objects = FieldBookQuerySet.as_manager()

    def __str__(self) -> str:
        return f"{self.name}"

    def get_absolute_url(self):
        return reverse("calculator:fieldbook_detail", args=(self.pk,))

    @classmethod
    def get_create_url(cls):
        return reverse("calculator:fieldbook_create")

    def get_update_url(self):
        return reverse("calculator:fieldbook_update", args=(self.pk,))

    def get_delete_url(self):
        return reverse("calculator:fieldbook_delete", args=[self.pk])

    @cached_property
    def is_deletable(self):
        if self.layout.is_archived:
            self.cant_delete_msg = "This FieldBook is archived."
            return False
        return (
            not Step.objects.filter(fieldbook=self)
            .filter(models.Q(traittarget__isnull=False) | models.Q(parametertarget__isnull=False))
            .exists()
        )

    def set_progress_counts(self):
        planned_target_count = 0
        observation_count = 0
        fulfilled_target_count = 0

        for step in self.steps_for_progress:
            trait_observation_counts = {}
            for observation in step.traitobservation.all():
                trait_id = observation.state.trait_id
                trait_observation_counts[trait_id] = trait_observation_counts.get(trait_id, 0) + 1

            parameter_observation_counts = {}
            for observation in step.parameterobservation.all():
                parameter_id = observation.parameter_id
                parameter_observation_counts[parameter_id] = parameter_observation_counts.get(parameter_id, 0) + 1

            observation_count += sum(trait_observation_counts.values()) + sum(parameter_observation_counts.values())
            for target in step.traittarget.all():
                planned_target_count += target.required_count
                fulfilled_target_count += min(target.required_count, trait_observation_counts.get(target.trait_id, 0))
            for target in step.parametertarget.all():
                planned_target_count += target.required_count
                fulfilled_target_count += min(
                    target.required_count,
                    parameter_observation_counts.get(target.parameter_id, 0),
                )

        self.planned_target_count = planned_target_count
        self.observation_count = observation_count
        self.percent_completed = 100.0 * fulfilled_target_count / planned_target_count if planned_target_count else 0.0

    def validate_display_config(self):
        display = self.display_config

        if display is None:
            return None

        if not isinstance(display, dict):
            raise ValueError("`display` must be a dictionary.")

        if "model" not in display or "id" not in display:
            raise ValueError("`display` must contain at least 'model' and 'id' keys")

        model = display["model"]
        if model not in {"trait", "parameter"}:
            raise ValueError("`display.model` must be either 'trait' or 'parameter'")

        if not isinstance(display["id"], int):
            raise ValueError("`display.id` must be an integer")

        if "field" in display and display["field"] not in {"value", "date"}:
            raise ValueError("`field` value must be either 'value' or 'date'")

        return display

    def set_display_config(self, model: str, id_: int, field: str = "value"):
        config = {"model": model, "id": id_, "field": field}
        self.display_config = config
        self.validate_display_config()

    def get_display_config_string(self):
        if self.display_config:
            return f"{self.display_config['model']}:{self.display_config['id']}:{self.display_config['field']}"
        return None


class StepQuerySet(models.QuerySet):
    def mutable(self):
        return self.filter(fieldbook__layout__archived_at__isnull=True)


class Step(models.Model):
    fieldbook = models.ForeignKey(FieldBook, on_delete=models.CASCADE, related_name="steps")
    crop = models.ForeignKey(Crop, on_delete=models.CASCADE, related_name="steps")
    order = models.PositiveIntegerField(default=0)

    objects = StepQuerySet.as_manager()

    class Meta:
        ordering = ("order",)
        unique_together = ("fieldbook", "crop")

    def __str__(self):
        return f"Step {self.order + 1}"

    def save(self, *args, **kwargs):
        self.full_clean()
        return super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse("calculator:step_detail", args=(self.pk,))

    def clean(self):
        super().clean()
        if self.fieldbook_id and self.crop_id and self.fieldbook.layout_id != self.crop.layout_id:
            raise ValidationError({"crop": "The crop must belong to the field book layout."})

    def previous(self):
        return (
            self.__class__.objects.filter(fieldbook_id=self.fieldbook_id, order__lt=self.order)
            .order_by("-order")
            .first()
        )

    def next(self):
        return (
            self.__class__.objects.filter(fieldbook_id=self.fieldbook_id, order__gt=self.order)
            .order_by("order")
            .first()
        )


class Target(models.Model):
    step = models.ForeignKey(Step, on_delete=models.CASCADE, related_name="%(class)s")
    required_count = models.PositiveSmallIntegerField(default=1)

    class Meta:
        abstract = True


class TraitTargetQuerySet(models.QuerySet):
    def mutable(self):
        return self.filter(step__fieldbook__layout__archived_at__isnull=True)


class TraitTarget(Target):
    trait = models.ForeignKey(Trait, on_delete=models.CASCADE)

    objects = TraitTargetQuerySet.as_manager()

    class Meta:
        constraints = [models.UniqueConstraint(fields=["step", "trait"], name="unique_trait_target_per_step")]

    def __str__(self):
        return f"{self.step}: {self.trait}"

    def save(self, *args, **kwargs):
        self.full_clean()
        return super().save(*args, **kwargs)

    def clean(self):
        super().clean()
        if self.step_id and self.trait_id and self.step.crop.variety.species_id != self.trait.protocol.plantspecies_id:
            raise ValidationError({"trait": "The trait species must match the crop variety species."})


class ParameterTargetQuerySet(models.QuerySet):
    def mutable(self):
        return self.filter(step__fieldbook__layout__archived_at__isnull=True)


class ParameterTarget(Target):
    parameter = models.ForeignKey(Parameter, on_delete=models.CASCADE)

    objects = ParameterTargetQuerySet.as_manager()

    class Meta:
        constraints = [models.UniqueConstraint(fields=["step", "parameter"], name="unique_parameter_target_per_step")]

    def __str__(self):
        return f"{self.step}: {self.parameter}"


class Observation(models.Model):
    crop = models.ForeignKey(Crop, on_delete=models.PROTECT, related_name="%(class)s")
    step = models.ForeignKey(Step, on_delete=models.SET_NULL, null=True, blank=True, related_name="%(class)s")
    recorded_at = models.DateTimeField(default=now)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name="%(class)s")
    notes = models.CharField(max_length=255, default="", blank=True)

    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        self.full_clean()
        return super().save(*args, **kwargs)

    def clean(self):
        super().clean()
        if self.step_id and self.crop_id and self.step.crop_id != self.crop_id:
            raise ValidationError({"crop": "The observation crop must match its step crop."})


class TraitObservationQuerySet(models.QuerySet):
    def mutable(self):
        return self.filter(crop__layout__archived_at__isnull=True)


class TraitObservation(Observation):
    state = models.ForeignKey(State, on_delete=models.PROTECT)

    objects = TraitObservationQuerySet.as_manager()

    class Meta:
        ordering = ("-recorded_at", "-pk")

    def __str__(self) -> str:
        return f"Expression recorded at {self.recorded_at} on Crop {self.crop_id}"

    @property
    def trait_id(self):
        return self.state.trait_id

    def clean(self):
        super().clean()
        if self.step_id:
            target = TraitTarget.objects.filter(step_id=self.step_id, trait_id=self.state.trait_id).exists()
            if not target:
                raise ValidationError({"state": "The state must belong to a trait targeted by this step."})


class ParameterObservationQuerySet(models.QuerySet):
    def mutable(self):
        return self.filter(crop__layout__archived_at__isnull=True)


class ParameterObservation(Observation):
    parameter = models.ForeignKey(Parameter, on_delete=models.PROTECT)
    parameter_value = models.DecimalField(max_digits=10, decimal_places=3, null=True, blank=True)
    parameter_date = models.DateField(null=True, blank=True)

    objects = ParameterObservationQuerySet.as_manager()

    class Meta:
        ordering = ("-recorded_at", "-pk")
        constraints = [
            models.CheckConstraint(
                condition=models.Q(parameter_value__isnull=False) | models.Q(parameter_date__isnull=False),
                name="at_least_one_of_value_or_date",
            )
        ]

    def __str__(self) -> str:
        return f"Parameter value recorded at {self.recorded_at} on Crop {self.crop_id}"

    def clean(self):
        super().clean()
        if self.step_id and self.parameter_id:
            target = ParameterTarget.objects.filter(step_id=self.step_id, parameter_id=self.parameter_id).exists()
            if not target:
                raise ValidationError({"parameter": "The parameter must be targeted by this step."})
