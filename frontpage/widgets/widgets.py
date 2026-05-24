from django.forms import TextInput
from django.forms.widgets import NumberInput

__all__ = [
    "YearInput",
    "BootstrapNumberInput",
    "BootstrapTextInput",
]


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


class BootstrapTextInput(TextInput):
    def __init__(self, attrs=None):
        default_attrs = {"class": "form-control"}
        if attrs:
            default_attrs.update(attrs)
        super().__init__(attrs=default_attrs)
