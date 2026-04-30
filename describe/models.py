"""Characterization-related models."""

from typing import Iterable

from django.contrib.auth.models import User
from django.db import models
from django.db.models import F, Prefetch, UniqueConstraint
from django.db.models.aggregates import Count
from django.db.models.functions import Coalesce
from django.db.utils import OperationalError, ProgrammingError
from django.urls import reverse
from django.utils.functional import cached_property

from frontpage.generic import ModelIsDeletableMixin
from frontpage.utils.models import connected_components
from register.models import PlantSpecies, PlantVariety

PREFETCHED_GROUP_STATES_ATTR_NAME = "prefetched_group_states"
PREFETCHED_RELATED_STATES_ATTR_NAME = "prefetched_related_states"


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

    @classmethod
    def get_create_url(cls):
        return reverse("describe:protocol_create")

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

        result = self.prefetch_related("expressions__state")

        for expressions in expressions_filter.values():
            result = result.filter(expressions__state__group__states__id__in=expressions)

        return result.distinct()

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

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    notes = models.CharField(max_length=500, help_text="Notes relative to the description", default="", blank=True)

    objects = DescriptionQuerySet.as_manager()

    class Meta:
        ordering = ("variety__name",)

    def __str__(self):
        return f"{self.variety.name} ({self.name})"

    def get_absolute_url(self):
        return reverse("describe:description_detail", args=(self.pk,))

    @classmethod
    def get_create_url(cls):
        return reverse("describe:description_create")

    def get_update_url(self):
        return reverse("describe:description_expression_update", args=(self.pk,))

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
        verbose_name="ID",
        help_text="Numbering code",
    )
    description = models.CharField(
        max_length=200,
        verbose_name="name",
        help_text="A descriptive, unique, and unambiguous name",
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
        constraints = [
            UniqueConstraint(
                "numeric_id",
                "protocol",
                name="unique_numeric_id_per_protocol",
                violation_error_message="Each protocol must have unique Descriptor IDs. This one is already used.",
            )
        ]

    def __str__(self):
        """Return string representation of a Trait as `ID. DESCRIPTION`."""
        return f"{self.numeric_id}. {self.description}"

    def is_deletable(self):
        return not Expression.objects.filter(state__in=self.states.all()).exists()

    def get_next_in_protocol(self):
        return Trait.objects.filter(protocol=self.protocol, numeric_id__gt=self.numeric_id).first()

    def get_previous_in_protocol(self):
        return Trait.objects.filter(protocol=self.protocol, numeric_id__lt=self.numeric_id).last()

    def states_with_related_states(self):
        """Return the trait's states, with their group relations prefetched.

        Use with `State.related()` to avoid queries duplication when
        rendering related states.  The group states are stored on each
        `StateGroup` in the attribute `PREFETCHED_GROUP_STATES_ATTR_NAME`.

        """
        State = self.states.model  # ty:ignore[unresolved-attribute]
        states_with_trait_protocol = State.objects.select_related("trait", "trait__protocol").order_by(
            "trait__protocol__order", "trait__numeric_id", "numeric_id"
        )
        prefetched_group_states = Prefetch(
            "group__states", queryset=states_with_trait_protocol, to_attr=PREFETCHED_GROUP_STATES_ATTR_NAME
        )
        prefetched_related_states = Prefetch(
            "related_states", State.objects.all(), to_attr=PREFETCHED_RELATED_STATES_ATTR_NAME
        )
        return self.states.select_related("group").prefetch_related(  # ty:ignore[unresolved-attribute]
            prefetched_group_states, prefetched_related_states
        )


class StateGroup(models.Model):
    """Store the grouping between States for relating Expressions from different Protocols."""

    def __str__(self):
        return f"StateGroup #{self.pk}"


class StateQuerySet(models.QuerySet):
    def rebuild_groups(self):
        state_ids = list(self.values_list("pk", flat=True))

        if not state_ids:
            return []

        through = self.model.related_states.through

        edges = list(
            through.objects.filter(
                from_state_id__in=state_ids,
                to_state_id__in=state_ids,
            ).values_list("from_state_id", "to_state_id")
        )

        components = connected_components(state_ids, edges)

        groups = []

        for component in components:
            group = StateGroup.objects.create()
            self.model.objects.filter(pk__in=component).update(group=group)
            groups.append(group)

        StateGroup.objects.filter(states__isnull=True).delete()

        return groups


class State(models.Model):
    """Store the possible states of expression of a Trait."""

    numeric_id = models.IntegerField(verbose_name="ID", help_text="Numbering code.")
    description = models.CharField(help_text="A descriptive text about the state.", max_length=200)
    trait = models.ForeignKey(Trait, models.CASCADE, related_name="states")
    related_states = models.ManyToManyField("self", symmetrical=True, blank=True)
    group = models.ForeignKey(StateGroup, on_delete=models.CASCADE, related_name="states")

    objects = StateQuerySet.as_manager()

    class Meta:
        unique_together = ("numeric_id", "trait")
        ordering = ("trait", "numeric_id")

    def __str__(self):
        """Return the string representation of a state as `ID. DESCRIPTION`."""
        return f"{self.numeric_id}. {self.description}"

    def is_deletable(self):
        return not Expression.objects.filter(state=self).exists()

    def related(self) -> Iterable["State"]:
        """Return only related states.

        Default to using prefetched States in
        `PREFETCHED_STATES_ATTR_NAME` attribute in `group` to avoid
        duplicating queries. This is intended to be used with
        `Trait.states_with_related_states()`.

        """

        prefetched = getattr(self.group, PREFETCHED_GROUP_STATES_ATTR_NAME, None)
        if prefetched is not None:
            return [state for state in prefetched if state.pk != self.pk]
        return self.group.states.exclude(pk=self.pk).select_related("trait", "trait__protocol")

    def reset_group(self):
        group = StateGroup.objects.create()
        self.group = group
        return group


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
