from django import forms


class TomSelectMixin:
    def __init__(self, attrs=None, choices=()):
        default_attrs = {
            "class": "form-select tomselect",
        }
        if attrs:
            default_attrs.update(attrs)
        super().__init__(attrs=default_attrs, choices=choices)


class TomSelect(TomSelectMixin, forms.Select):
    """TomSelect for single choice fields."""


class TomSelectMultiple(TomSelectMixin, forms.SelectMultiple):
    """TomSelect for multiple choice fields."""
