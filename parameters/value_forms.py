"""Type-specific value inputs shared by reference and observation forms."""

from django import forms

from frontpage.widgets import UnitNumberInput

from .models import Parameter
from .values import VALUE_FIELDS


class TypedValueBoundField(forms.BoundField):
    def css_classes(self, extra_classes=None):
        return f"{super().css_classes(extra_classes)} typed-value-field".strip()


class TypedValueFormMixin:
    def __init__(self, *args, parameter=None, parameter_refresh_url=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.parameter_obj = parameter
        if self.parameter_obj is None:
            parameter_id = (
                (self.data.get(self.add_prefix("parameter")) if self.is_bound else self.initial.get("parameter"))
                if "parameter" in self.fields
                else self.instance.parameter_id
            )
            if isinstance(parameter_id, Parameter):
                self.parameter_obj = parameter_id
            elif parameter_id:
                try:
                    self.parameter_obj = Parameter.objects.filter(pk=parameter_id).first()
                except (ValueError, TypeError):
                    pass
            elif self.instance.parameter_id:
                self.parameter_obj = self.instance.parameter
        selected = f"value_{self.parameter_obj.type}" if self.parameter_obj else None
        for field in VALUE_FIELDS:
            if field != selected:
                self.fields.pop(field, None)
        if selected:
            field = self.fields[selected]
            field.label = "Value"
            field.required = True
            if self.parameter_obj.type == "boolean":
                self.fields[selected] = forms.TypedChoiceField(
                    choices=(("", "Choose…"), ("True", "Yes"), ("False", "No")),
                    coerce=lambda value: value == "True",
                    label="Value",
                )
            elif self.parameter_obj.type == "date":
                field.widget = forms.DateInput(attrs={"type": "date"})
            elif self.parameter_obj.type in {"integer", "decimal"} and self.parameter_obj.measure_unit:
                field.widget = UnitNumberInput(self.parameter_obj.measure_unit, attrs=field.widget.attrs)
        else:
            self.fields["value_placeholder"] = forms.CharField(
                label="Value",
                required=False,
                disabled=True,
                widget=forms.TextInput(attrs={"placeholder": "Select a parameter first"}),
            )
            field_order = list(self.fields)
            field_order.remove("value_placeholder")
            position = field_order.index("parameter") + 1 if "parameter" in field_order else 0
            field_order.insert(position, "value_placeholder")
            self.order_fields(field_order)
        value_field_name = selected or "value_placeholder"
        self.fields[value_field_name].bound_field_class = TypedValueBoundField
        if (
            parameter_refresh_url
            and "parameter" in self.fields
            and not isinstance(self.fields["parameter"].widget, forms.HiddenInput)
        ):
            self.fields["parameter"].widget.attrs.update(
                {
                    "hx-get": parameter_refresh_url,
                    "hx-include": "closest form",
                    "hx-target": "next .typed-value-field",
                    "hx-select": f"form:has([name='{self.add_prefix('parameter')}']) .typed-value-field",
                    "hx-swap": "outerHTML",
                    "hx-trigger": "change",
                }
            )

    @property
    def value_field(self):
        if self.parameter_obj:
            return self[f"value_{self.parameter_obj.type}"]
        return self["value_placeholder"]

    def clean(self):
        cleaned = super().clean()
        if "parameter" in self.fields and "parameter" not in cleaned:
            self.instance.parameter = None
        # Removed model fields must not retain values from a previously selected parameter.
        for field in VALUE_FIELDS:
            if field not in self.fields:
                setattr(self.instance, field, None)
        return cleaned
