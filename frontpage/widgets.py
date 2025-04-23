from django.forms.widgets import NumberInput, Select, SelectMultiple


class TomSelectMixin:
    def __init__(self, attrs=None, choices=()):
        default_attrs = {
            "class": "form-select tomselect",
        }
        if attrs:
            default_attrs.update(attrs)
        super().__init__(attrs=default_attrs, choices=choices)


class TomSelect(TomSelectMixin, Select):
    """TomSelect for single choice fields."""


class TomSelectMultiple(TomSelectMixin, SelectMultiple):
    """TomSelect for multiple choice fields."""


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
