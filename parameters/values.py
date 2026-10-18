"""Shared storage and validation for parameter reference values and observations."""

from django.core.exceptions import ValidationError
from django.db import models

VALUE_FIELDS = tuple(f"value_{kind}" for kind in ("boolean", "integer", "decimal", "date", "text"))


def validate_typed_value(parameter, values):
    populated = [field for field in VALUE_FIELDS if values.get(field) is not None]
    expected = f"value_{parameter.type}"
    if populated != [expected]:
        raise ValidationError({"__all__": f"Provide exactly one {parameter.type} value for this parameter."})
    if parameter.type == "text" and not values[expected].strip():
        raise ValidationError({expected: "A text value cannot be empty."})


def exactly_one_value():
    condition = models.Q()
    for selected in VALUE_FIELDS:
        condition |= models.Q(**{f"{field}__isnull": field != selected for field in VALUE_FIELDS})
    return condition


class TypedValue(models.Model):
    value_boolean = models.BooleanField(null=True, blank=True)
    value_integer = models.BigIntegerField(null=True, blank=True)
    value_decimal = models.DecimalField(max_digits=20, decimal_places=10, null=True, blank=True)
    value_date = models.DateField(null=True, blank=True)
    value_text = models.TextField(null=True, blank=True)  # noqa: DJ001 - NULL denotes an unused typed column.

    class Meta:
        abstract = True
        constraints = [
            models.CheckConstraint(condition=exactly_one_value(), name="%(app_label)s_%(class)s_one_value"),
        ]

    def clean(self):
        super().clean()
        if not self._state.adding:
            original_parameter_id = (
                type(self).objects.using(self._state.db).values_list("parameter_id", flat=True).get(pk=self.pk)
            )
            if self.parameter_id != original_parameter_id:
                raise ValidationError({"parameter": "Parameter cannot be changed after creation."})
        if self.parameter_id:
            validate_typed_value(self.parameter, {field: getattr(self, field) for field in VALUE_FIELDS})

    @property
    def value(self):
        return getattr(self, f"value_{self.parameter.type}")

    def get_value_display(self):
        value = self.value
        if self.parameter.type == "boolean":
            return "Yes" if value else "No"
        if self.parameter.type == "decimal" and value is not None:
            value = format(value, "f")
            if "." in value:
                value = value.rstrip("0").rstrip(".")
        unit = self.parameter.measure_unit if self.parameter.type in {"integer", "decimal"} else ""
        return f"{value} {unit}".strip()
