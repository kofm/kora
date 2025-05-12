"""Characterization-related models."""

from django.contrib.auth.models import User
from django.db import models
from django.db.models import F
from django.db.models.aggregates import Count
from django.db.models.functions import Coalesce
from django.db.models.query_utils import Q
from django.db.utils import OperationalError, ProgrammingError
from django.urls import reverse
from django.utils.functional import cached_property

from frontpage.generic import ModelIsDeletableMixin
from register.models import PlantSpecies, PlantVariety


class ProtocolManager(models.Manager):
    def most_used(self):
        if Protocol.objects.count() > 0:
            return self.annotate(count=Coalesce(Count("descriptions"), 0)).order_by("-count").first()
        return None


class Protocol(ModelIsDeletableMixin, models.Model):
    """A Protocol is a list of descriptors (Trait)."""

    name = models.CharField(max_length=200, help_text="the name of the protocol")
    plantspecies = models.ForeignKey(
        PlantSpecies,
        on_delete=models.PROTECT,
        verbose_name="Species",
        help_text="reference to the specie it is meant to use with",
    )
    url_ref = models.URLField(verbose_name="URL", blank=True, default="", help_text="the URL reference to the protocol")
    order = models.PositiveIntegerField(default=0)
    objects = ProtocolManager()

    class Meta:
        ordering = ("order", "name")

    def __str__(self):
        return f"{self.name}"

    def get_absolute_url(self):
        return reverse("describe:protocol_detail", kwargs={"pk": self.pk})

    def get_update_url(self):
        return reverse("describe:protocol_update", args=(self.pk,))

    def get_delete_url(self):
        return reverse("describe:protocol_delete", args=(self.pk,))

    def with_traits_and_states(self):
        return Trait.objects.filter(protocol=self.pk).prefetch_related("states").order_by("numeric_id")


class DescriptionQuerySet(models.QuerySet):
    def filter_by_expressions(self, expressions_filter: dict):
        """Filter Descriptions by Expression.

        Multiple values for the same Trait are considered as
        alternatives (OR).

        Values referring to different Traits are considered as
        conjunctions (AND).

        Example:

        For the same trait (e.g., "Stem: length"), multiple values
        like "short" and "medium" are treated as alternatives (OR) -
        meaning either "short" OR "medium" will match.

        For different traits (e.g., "Stem: length" AND "Flower:
        color"), the conditions are treated as conjunctions (AND) -
        meaning both conditions must be satisfied for a match.

        An empty filter will return zero Description.
        """
        if not expressions_filter:
            return self.none()

        expressions_list = [val for key, val in expressions_filter.items()]

        def get_filter_query(expressions: list) -> Q:
            query = Q(expressions__state__id__in=expressions)
            query |= Q(expressions__state__related_states__id__in=expressions)

            return query

        query = get_filter_query(expressions_list[0])

        result = self.prefetch_related("expressions__state").filter(query).distinct()

        for expressions in expressions_list[1:]:
            query = get_filter_query(expressions)
            query_set = self.filter(query).distinct()
            result = result.intersection(query_set)

        return result

    def with_expressions(self):
        return (
            self.select_related("variety", "protocol", "variety__species")
            .prefetch_related("expressions", "protocol__traits")
            .all()
        )

    def annotated(self):
        return (
            self.select_related("variety__species")
            .select_related("protocol__plantspecies")
            .prefetch_related("expressions")
            .values(
                "variety__id",
                "variety__name",
                "name",
                species_id=F("protocol__plantspecies__id"),
                species_name=F("protocol__plantspecies__common_name"),
                state_id=F("expressions__state__id"),
                note=F("expressions__note"),
            )
            .order_by(
                "species_id",
                "species_name",
                "variety__id",
                "variety__name",
                "name",
            )
        )


class Description(ModelIsDeletableMixin, models.Model):
    name = models.CharField(verbose_name="tag", max_length=200, help_text="The identifier of the description")
    protocol = models.ForeignKey(
        Protocol,
        on_delete=models.PROTECT,
        help_text="Reference protocol used to make the description;\
            this will define which Traits will be available",
        related_name="descriptions",
    )
    variety = models.ForeignKey(
        PlantVariety,
        on_delete=models.RESTRICT,
        help_text="The variety to which the description refers to",
    )

    objects = DescriptionQuerySet.as_manager()

    class Meta:
        ordering = ("variety__name",)

    def __str__(self):
        return f"{self.variety.name} ({self.name})"

    def get_absolute_url(self):
        return reverse("describe:description_detail", args=(self.pk,))

    def get_update_url(self):
        return reverse("describe:description_update", args=(self.pk,))

    def get_delete_url(self):
        return reverse("describe:description_delete", args=(self.pk,))

    @classmethod
    def names(cls):
        try:
            queryset = cls.objects.order_by("name").values_list("name", flat=True).distinct()
            return [(name, name) for name in queryset]
        except (ProgrammingError, OperationalError):
            return []

    @cached_property
    def available_traits(self):
        return self.protocol.traits.all()


class TraitQuerySet(models.QuerySet):
    def with_states(self):
        return self.prefetch_related("states").order_by("numeric_id")


class Trait(models.Model):
    numeric_id = models.IntegerField(
        null=True,
        blank=True,
        verbose_name="ID",
        help_text="Numbering code.",
    )
    description = models.CharField(
        max_length=200,
        verbose_name="name",
        help_text="A descriptive, unique, and unambiguous name.",
    )
    protocol = models.ForeignKey(
        Protocol,
        on_delete=models.CASCADE,
        related_name="traits",
        help_text="The reference protocol of the trait",
    )
    grouping = models.BooleanField(default=False, help_text="Is this a highly discriminating characteristic?")

    objects = TraitQuerySet.as_manager()

    class Meta:
        ordering = ("numeric_id",)

    def __str__(self):
        """Return string representation of a Trait as `ID. DESCRIPTION`."""
        return f"{self.numeric_id}. {self.description}"

    def is_deletable(self):
        return not Expression.objects.filter(state__in=self.states.all()).exists()

    def get_next_in_protocol(self):
        return Trait.objects.filter(protocol=self.protocol, numeric_id__gt=self.numeric_id).first()

    def get_previous_in_protocol(self):
        return Trait.objects.filter(protocol=self.protocol, numeric_id__lt=self.numeric_id).last()


class State(models.Model):
    """Store the possible states of expression related to a Trait."""

    numeric_id = models.IntegerField(verbose_name="ID", help_text="Numbering code.")
    description = models.CharField(help_text="A descriptive text about the state.", max_length=200)
    trait = models.ForeignKey(Trait, models.CASCADE, related_name="states")
    related_states = models.ManyToManyField("self")

    class Meta:
        unique_together = ("numeric_id", "trait")
        ordering = ("trait", "numeric_id")

    def __str__(self):
        """Return the string representation of a state as `ID. DESCRIPTION`."""
        return f"{self.numeric_id}. {self.description}"

    def is_deletable(self):
        return not Expression.objects.filter(state=self).exists()


class Expression(models.Model):
    """Store the variety state of expression related to a specific trait within a Description.

    It refers to a specific State of expression (which is, in turn, related to a
    specific Trait).
    """

    state = models.ForeignKey(State, on_delete=models.PROTECT)
    description = models.ForeignKey(Description, on_delete=models.CASCADE, related_name="expressions")
    note = models.CharField(max_length=512, blank=True, help_text="Add any additional information here.")

    class Meta:
        ordering = ("state__trait__numeric_id",)

    def __str__(self):
        """Return the string representation of the Expression instance."""
        return self.state.__str__()

    def trait(self):
        """Return the trait related to the Expression' State."""
        return self.state.trait


class WorkspaceQuerySet(models.QuerySet):
    def elements(self):
        return self.prefetch_related(
            "descriptions",
            "descriptions__description",
            "descriptions__description__protocol",
            "descriptions__description__variety",
            "descriptions__description__variety__species",
        )

    def deactivate_all(self):
        return self.update(is_active=False)


class Workspace(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=200, help_text="The identificative name of the list")
    is_active = models.BooleanField(default=False)

    objects = WorkspaceQuerySet.as_manager()

    def __str__(self) -> str:
        return self.name

    def save(self, *args, **kwargs):
        if self.is_active:
            Workspace.objects.filter(user=self.user).exclude(pk=self.pk).update(is_active=False)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse("describe:description_compare")


class WorkspaceElement(models.Model):
    workspace = models.ForeignKey(Workspace, on_delete=models.CASCADE, related_name="descriptions")
    description = models.ForeignKey(Description, on_delete=models.CASCADE)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        unique_together = ("description", "workspace")
        ordering = ("order",)

    def __str__(self) -> str:
        return str(self.description)
