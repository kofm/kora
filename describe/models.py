"""Characterization-related models."""

from django.contrib.auth.models import User
from django.db import models
from django.db.models import QuerySet
from django.db.models.aggregates import Count
from django.db.models.functions import Coalesce, Concat
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
    objects = ProtocolManager()

    class Meta:
        ordering = ("name",)

    def __str__(self):
        return f"{self.name} ({self.plantspecies.latin_name})"

    def get_absolute_url(self):
        return reverse("describe:protocol_detail", kwargs={"pk": self.pk})

    def get_update_url(self):
        return reverse("describe:protocol_update", args=(self.pk,))

    def get_delete_url(self):
        return reverse("describe:protocol_delete", args=(self.pk,))

    def traits_list(self):
        return self.traits.all().order_by("numeric_id").values("pk", "numeric_id", "description")

    def traits_states_list(self):
        state_description_annotation = {
            "state_description": Concat(
                "numeric_id",
                models.Value(". "),
                "description",
                output_field=models.CharField(),
            )
        }
        return [
            {
                "pk": trait["pk"],
                "numeric_id": trait["numeric_id"],
                "description": trait["description"],
                "states": list(
                    State.objects.filter(trait=trait["pk"])
                    .annotate(**state_description_annotation)
                    .values("pk", "numeric_id", "state_description")
                ),
            }
            for trait in self.traits_list()
        ]


class DescriptionManager(models.Manager):
    def filter_by_expressions(self, expressions_filter: list[dict[str, list]]) -> QuerySet:
        description_ids = None
        for flt in expressions_filter:
            query_result = self.filter(
                models.Q(expressions__state__id__in=flt["state"])
                | models.Q(expressions__state__related_states__id__in=flt["state"])
            ).values_list("pk", flat=True)
            description_ids = query_result if description_ids is None else description_ids.intersection(query_result)
        return self.filter(pk__in=list(description_ids)).select_related("variety").select_related("protocol")


class Description(ModelIsDeletableMixin, models.Model):
    """Stores the Descriptions.

    A description is a collection of Expressions.
    """

    name = models.CharField(max_length=200, help_text="The identifier of the description")
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

    objects = DescriptionManager()

    class Meta:
        ordering = ("variety__name",)

    def __str__(self):
        return f"{self.variety} ({self.name} description)"

    def get_absolute_url(self):
        return reverse("describe:description_detail", args=(self.pk,))

    def get_update_url(self):
        return reverse("describe:description_update", args=(self.pk,))

    def get_delete_url(self):
        return reverse("describe:description_delete", args=(self.pk,))

    @classmethod
    def names(cls):
        queryset = cls.objects.all().order_by("name").values_list("name", flat=True).distinct("name")
        return [(name, name) for name in queryset]

    @cached_property
    def available_traits(self):
        return self.protocol.traits.all()


class Trait(models.Model):
    """Store the Traits.

    Traits can have multiple states of expression.
    """

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

    class Meta:
        """Trait model Meta class."""

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


class Workspace(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=200, help_text="The identificative name of the list")
    is_active = models.BooleanField(default=False)

    def __str__(self) -> str:
        return self.name

    def save(self, *args, **kwargs):
        if self.is_active:
            Workspace.objects.filter(user=self.user).exclude(pk=self.pk).update(is_active=False)
        super().save(*args, **kwargs)


class WorkspaceElement(models.Model):
    workspace = models.ForeignKey(Workspace, on_delete=models.CASCADE, related_name="descriptions")
    description = models.ForeignKey(Description, on_delete=models.CASCADE)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        unique_together = ("description", "workspace")
        ordering = ("order",)

    def __str__(self) -> str:
        return str(self.description)
