"""Models to create cultivars' descriptions

These are the models related to the describe app, responsible of creating
cultivars' descriptions.
"""

from django.db import models
from django.db.models.aggregates import Count
from django.db.models.functions import Coalesce
from django.urls import reverse
from django.utils.functional import cached_property

from register.models import PlantSpecies, PlantVariety


class ProtocolManager(models.Manager):
    def most_used(self):
        return (
            self.annotate(count=Coalesce(Count("descriptions"), 0))
            .order_by("-count")
            .first()
        )


class Protocol(models.Model):
    """
    Stores a Protocols used in descriptions. It is basically a collection
    of traits.
    """

    name = models.CharField(max_length=200, help_text="the name of the protocol")
    plantspecies = models.ForeignKey(
        PlantSpecies,
        on_delete=models.PROTECT,
        help_text="reference to the specie it is meant to use with",
    )
    url_ref = models.URLField(
        blank=True, null=True, help_text="the URL reference to the protocol"
    )
    objects = ProtocolManager()

    def get_absolute_url(self):
        return reverse("describe:protocol_detail", kwargs={"pk": self.pk})

    def __str__(self):
        return f"{self.name} ({self.plantspecies.latin_name})"


class Description(models.Model):
    """
    Stores the Descriptions. A description is a collection of Expresions
    """

    name = models.CharField(
        max_length=200, help_text="the name/identifier of the description"
    )
    protocol = models.ForeignKey(
        Protocol,
        on_delete=models.PROTECT,
        help_text="reference to the protocol used to make the description;\
            this will define which Traits will be available",
        related_name="descriptions",
    )
    variety = models.ForeignKey(
        PlantVariety,
        on_delete=models.RESTRICT,
        help_text="the variety to which the description refers to",
    )

    class Meta:
        ordering = ["variety__name"]

    @cached_property
    def available_traits(self):
        return self.protocol.traits.all()

    def filter_by_expression(self, states: list, queryset = None):
        if not queryset:
            queryset = self.objects.all().prefetch_related("expressions")
        return queryset.filter(expressions__state__in=states)

    def get_absolute_url(self):
        return reverse("describe:description_detail", kwargs={"pk": self.pk})

    def __str__(self):
        return f"{self.variety} ({self.name} description)"


class Trait(models.Model):
    """
    Stores the Traits. Each traits can have multiple States of expression
    """

    numeric_id = models.IntegerField(
        null=True,
        blank=True,
        help_text="The numeric identifier of the trait",
    )
    description = models.CharField(
        max_length=200,
        help_text="The trait's description",
    )
    protocol = models.ForeignKey(
        Protocol,
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        related_name="traits",
        help_text="The reference protocol of the trait",
    )
    grouping = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.numeric_id}. {self.description}"

    class Meta:
        ordering = [
            "numeric_id",
        ]


class State(models.Model):
    """
    Stores the different States of expression related to a Trait.
    """

    numeric_id = models.IntegerField(
        help_text="a numeric ID that can be associated with the trait",
        null=True,
        blank=True,
    )
    description = models.CharField(max_length=200, null=False, blank=False)
    trait = models.ForeignKey(Trait, models.CASCADE)

    def __str__(self):
        return f"{self.numeric_id}. {self.description}"

    class Meta:
        ordering = [
            "numeric_id",
        ]


class Expression(models.Model):
    """
    Stores the expression of cultivars, related to a specific Description. It
    refers to a specific State of expression (which is then related to a
    specific Trait)
    """

    state = models.ForeignKey(State, on_delete=models.PROTECT)
    description = models.ForeignKey(
        Description, on_delete=models.CASCADE, related_name="expressions"
    )

    def __str__(self):
        return self.state.__str__()
