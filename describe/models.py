"""Models to create cultivars' descriptions

These are the models related to the describe app, responsible of creating
cultivars' descriptions.
"""

from django.db import models
from django.utils.functional import cached_property

from register.models import PlantSpecies, PlantVariety


class Protocol(models.Model):
    """
    Stores a Protocols used in descriptions. It is basically a collection
    of traits.
    """

    name = models.CharField(max_length=200, help_text="the name of the protocol")
    specie = models.ForeignKey(
        PlantSpecies,
        on_delete=models.PROTECT,
        help_text="reference to the specie it is meant to use with",
    )
    url_ref = models.URLField(
        blank=True, null=True, help_text="the URL reference to the protocol"
    )

    def __str__(self):
        return self.name


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
    )
    variety = models.ForeignKey(
        PlantVariety,
        on_delete=models.RESTRICT,
        help_text="the variety to which the description refers to",
    )

    class Meta:
        ordering = ['variety__name']

    @cached_property
    def available_traits(self):
        return self.protocol.traits.all()

    def __str__(self):
        return str(self.variety) + " (" + self.name + ")"


class Trait(models.Model):
    """
    Stores the Traits. Each traits can have multiple States of expression
    """

    numeric_id = models.IntegerField(
        null=True,
        blank=True,
        help_text="the numeric identifier often used in official \
                    protocols",
    )
    # TODO: this can be removed?
    description = models.CharField(
        max_length=200,
        help_text="trait description",
    )
    protocol = models.ForeignKey(
        Protocol, on_delete=models.PROTECT, null=True, blank=True, related_name="traits"
    )

    def __str__(self):
        return str(self.numeric_id) + ". " + self.description

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
    # TODO: REMOVE THIS!!
    description = models.CharField(max_length=200, null=False, blank=False)
    trait = models.ForeignKey(Trait, models.CASCADE)

    def __str__(self):
        return str(self.numeric_id) + ". " + self.description

    class Meta:
        ordering = [
            "numeric_id",
        ]


class Expression(models.Model):
    """
    Stores the expression of cultivars, related to a specific Description.
    It refers to a specific Traits and contain the actual State of
    expression for that Trait.
    """

    state_of_expression = models.ForeignKey(State, on_delete=models.PROTECT)
    description = models.ForeignKey(
        Description, on_delete=models.CASCADE, related_name="expressions"
    )

    def __str__(self):
        return str(self.state_of_expression)
