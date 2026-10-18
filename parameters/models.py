"""
These are the models related to storage of parameters and field measures
"""

from django.core.exceptions import ValidationError
from django.db import models
from django.urls import reverse

from frontpage.generic import ModelIsDeletableMixin
from register.models import PlantVariety

from .values import TypedValue


class ParameterManager(models.Manager):
    def get_by_natural_key(self, code):
        return self.get(code=code)


class Parameter(ModelIsDeletableMixin, models.Model):
    """
    Stores the parameters related to the Species. Parameters are inputs on which Crop
    Models rely on. This class defines the available parameters. The actual values are
    stored in ParameterValue objects, that reference one Parameter.
    """

    class Type(models.TextChoices):
        BOOLEAN = "boolean", "Boolean"
        INTEGER = "integer", "Integer"
        DECIMAL = "decimal", "Decimal"
        DATE = "date", "Date"
        TEXT = "text", "Text"

    type = models.CharField(max_length=7, choices=Type.choices, default=Type.DECIMAL)
    code = models.CharField(max_length=50, help_text="A code to identify the parameter.", unique=True)
    name = models.CharField(max_length=200, help_text="The name of the parameter.")
    description = models.CharField(max_length=200, help_text="The description of the parameter.")
    measure_unit = models.CharField(max_length=50, blank=True, help_text="The unit of measurement.")

    objects = ParameterManager()

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.full_clean()
        return super().save(*args, **kwargs)

    def get_absolute_url(self):
        return f"{reverse('parameters:varietalparameter_list')}?parameter={self.pk}"

    @classmethod
    def get_create_url(cls):
        return reverse("parameters:parameter_create")

    def get_update_url(self):
        return reverse("parameters:parameter_update", args=(self.pk,))

    def get_delete_url(self):
        return reverse("parameters:parameter_delete", args=(self.pk,))

    def natural_key(self):
        return (self.code,)

    def clean(self):
        super().clean()
        if not self._state.adding:
            original_type = type(self).objects.get(pk=self.pk).type
            if self.type != original_type:
                raise ValidationError(
                    {"type": "Parameter type cannot be changed. Delete and recreate unused parameters."}
                )


class ParameterValue(TypedValue):
    """
    Abstract class for parameters values
    """

    url_ref = models.URLField(help_text="a url reference for the source of the parameter", blank=True, default="")
    parameter = models.ForeignKey(Parameter, on_delete=models.RESTRICT)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    note = models.CharField(max_length=512, blank=True, help_text="Add any additional information here.")

    class Meta(TypedValue.Meta):
        abstract = True
        ordering = ["updated_at"]

    def __str__(self):
        return self.parameter.code

    def save(self, *args, **kwargs):
        self.full_clean()
        return super().save(*args, **kwargs)


class VarietalParameter(ParameterValue):
    """
    Varietal parameters values
    """

    variety = models.ForeignKey(PlantVariety, on_delete=models.RESTRICT, related_name="parameters")

    class Meta(ParameterValue.Meta):
        abstract = False
        ordering = ["created_at"]
        verbose_name = "value"
        verbose_name_plural = "values"

    @classmethod
    def get_create_url(cls):
        return reverse("parameters:varietalparameter_create")
