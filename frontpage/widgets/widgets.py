from django.forms import TextInput
from django.forms.widgets import NumberInput

__all__ = ("YearInput", "BootstrapNumberInput", "BootstrapTextInput", "UnitNumberInput")


class YearInput(NumberInput):
    def __init__(self, attrs=None):
        default_attrs = {
            "inputmode": "numeric",
            "autocomplete": "off",
            "min": "1900",
            "max": "2100",
            "class": "numberinput form-control",
        }
        if attrs:
            default_attrs.update(attrs)
        super().__init__(attrs=default_attrs)


class BootstrapNumberInput(NumberInput):
    def __init__(self, attrs=None):
        default_attrs = {"class": "form-control"}
        if attrs:
            default_attrs.update(attrs)
        super().__init__(attrs=default_attrs)


class UnitNumberInput(NumberInput):
    template_name = "frontpage/widgets/unit_number.html"

    def __init__(self, unit, attrs=None):
        self.unit = unit
        super().__init__(attrs=attrs)

    def get_context(self, name, value, attrs):
        context = super().get_context(name, value, attrs)
        widget = context["widget"]
        # Names include form prefixes, also providing a fallback when auto_id is off.
        addon_id = f"{widget['attrs'].get('id') or name}_unit"
        descriptions = widget["attrs"].get("aria-describedby", "").split()
        if addon_id not in descriptions:
            descriptions.append(addon_id)
        widget["attrs"]["aria-describedby"] = " ".join(descriptions)
        context.update(
            unit=self.unit,
            addon_id=addon_id,
            is_invalid="is-invalid" in widget["attrs"].get("class", "").split(),
        )
        return context


class BootstrapTextInput(TextInput):
    def __init__(self, attrs=None):
        default_attrs = {"class": "form-control"}
        if attrs:
            default_attrs.update(attrs)
        super().__init__(attrs=default_attrs)
