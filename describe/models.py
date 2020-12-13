"""Models to create cultivars' descriptions

These are the models related to the describe app, responsible of creating
cultivars' descriptions.
"""

from django.db import models
from register.models import PlantVariety,PlantSpecies

class Protocol(models.Model):
    """
    Stores a Protocols used in descriptions. It is basically a collection
    of traits.
    """
    name = models.CharField(
            max_length=200,
            help_text="the name of the protocol"
            )
    specie = models.ForeignKey(
            PlantSpecies,
            on_delete=models.PROTECT,
            help_text="reference to the specie it is meant to use with"
            )
    url_ref = models.URLField(
            blank=True, null=True,
            help_text="the URL reference to the protocol"
            )

    def __str__(self):
        return self.name

class Description(models.Model):
    """
    Stores the Descriptions. A description is a collection of Expresions
    """
    name = models.CharField(
            max_length=200,
            help_text="the name/identifier of the description")
    protocol = models.ForeignKey(
            Protocol,
            on_delete=models.PROTECT,
            help_text="reference to the protocol used to make the description;\
            this will define which Traits will be available"
            )
    variety = models.ForeignKey(
            PlantVariety,
            on_delete=models.RESTRICT,
            help_text="the variety to which the description refers to"
            )

    def __str__(self):
        return str(self.variety) + ' (' + self.name + ')'

class Trait(models.Model):
    """
    Stores the Traits. Each traits can have multiple States of expression
    """
    numeric_id = models.IntegerField(
            null=True, blank=True,
            help_text="the numeric identifier often used in official \
                    protocols"
                    )
    description = models.CharField(
            max_length=200,
            help_text="trait description"
            )
    protocol = models.ForeignKey(
            Protocol,
            on_delete=models.PROTECT,
            null = True, blank=True
            )

    def __str__(self):
        return str(self.numeric_id) + '. ' + self.description

class State(models.Model):
    """
    Stores the different States of expression related to a Trait.
    """
    numeric_id = models.IntegerField(
        help_text="a numeric ID that can be associated with the trait",
        null=True,blank=True
        )
    description = models.CharField(max_length=200)
    trait = models.ForeignKey(Trait, models.PROTECT)

    def __str__(self):
        return str(self.numeric_id) + '. ' + self.description

class Expression(models.Model):
    """
    Stores the expression of cultivars, related to a specific Description.
    It refers to a specific Traits and contain the actual State of 
    expression for that Trait.
    """
    recording_date = models.DateField()
    georeference_lat = models.FloatField()
    georeference_lon = models.FloatField()
    state_of_expression = models.ForeignKey(State, on_delete=models.PROTECT)
    description = models.ForeignKey(Description, on_delete=models.RESTRICT)

    def __str__(self):
        return str(self.state_of_expression) + \
                " (" + str(self.recording_date) + ")"

class Measure(models.Model):
    linked_trait = models.ForeignKey(Trait, on_delete=models.PROTECT)
    georeference_lat = models.FloatField()
    georeference_lon = models.FloatField()
    measure_unit = models.CharField(max_length=50)
    value = models.FloatField()
