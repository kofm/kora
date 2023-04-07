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
        if Protocol.objects.count() > 0:
            return (
                self.annotate(count=Coalesce(Count("descriptions"), 0))
                .order_by("-count")
                .first()
            )
        else:
            return None


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


class DescriptionManager(models.Manager):
    def filter_by_expression(self, filters):
        description_ids = None
        for filter in filters:
            query_result = self.filter(
                models.Q(expressions__state__id__in=filter["state"])
                | models.Q(expressions__state__related_states__id__in=filter["state"])
            ).values_list("pk", flat=True)
            if description_ids == None:
                description_ids = query_result
            else:
                description_ids = description_ids.intersection(query_result)
        return (
            self.filter(pk__in=list(description_ids))
            .select_related("variety")
            .select_related("protocol")
        )


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

    objects = DescriptionManager()

    class Meta:
        ordering = ["variety__name"]

    @cached_property
    def available_traits(self):
        return self.protocol.traits.all()

    def get_absolute_url(self):
        return reverse("describe:description-detail", kwargs={"pk": self.pk})

    def __str__(self):
        return f"{self.variety} ({self.name} description)"


class Trait(models.Model):
    """
    Stores the Traits. Each traits can have multiple States of expression
    """

    numeric_id = models.IntegerField(
        null=True,
        blank=True,
        help_text="The characteristic's numeric ID",
    )
    description = models.CharField(
        max_length=200,
        help_text="The characteristic's description",
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
        help_text="the numeric ID of the Note",
        null=True,
        blank=True,
    )
    description = models.CharField(
        help_text="A descriptive text about the note",
        max_length=200,
        null=False,
        blank=False
    )
    trait = models.ForeignKey(Trait, models.CASCADE, related_name="states")
    related_states = models.ManyToManyField("self")

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
