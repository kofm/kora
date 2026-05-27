"""Fields and widgets to declare TomSelect.js inputs in forms."""

import json

from django.forms.widgets import Select, SelectMultiple

__all__ = (
    "TomSelectConfig",
    "TomSelectMixin",
    "TomSelectLabel",
    "TomSelectLabelMultiple",
    "EmptySelect",
    "EmptySelectMultiple",
    "ModelTomSelect",
    "ModelTomSelectMultiple",
    "TomSelect",
    "TomSelectMultiple",
)


class TomSelectConfig:
    """Represents configuration for a TomSelect.js-powered form input.

    Leverage Django's `attrs` arguments from form fields, but extends
    its functionality to also allow lists and dictionaries. Set
    options are stored in in dataset properties of of the associated
    HTML element for Javascript processing. Used with TomSelect*
    classes allow declarative syntax to instantiate TomSelect
    elements.

    """

    defaults = {
        "max_options": 100,
        "preload": "true",
    }

    def __init__(self, **options):
        self.options = {
            **self.defaults,
            **options,
        }

    def attrs(self):
        return {f"data-ts-{self._to_kebab(key)}": self._serialize(value) for key, value in self.options.items()}

    def _serialize(self, value):
        if isinstance(value, (list | dict)):
            return json.dumps(value)
        return value

    @staticmethod
    def _to_kebab(value):
        return value.replace("_", "-")

    def depends_on(self):
        return self.options.get("depends_on")

    def depends_param(self):
        return self.options.get("depends_param")


class TomSelectMixin:
    """Merges TomSelectConfig specifications into the widget attributes and sets `tomselect` class."""

    ts_config = TomSelectConfig()

    def __init__(self, ts_config=None, attrs=None, choices=()):
        attrs = {} if attrs is None else attrs.copy()
        self.ts_config = ts_config if ts_config else self.ts_config
        attrs = self.build_attrs(attrs, {"class": "tomselect"})
        attrs = self.build_attrs(attrs, self.ts_config.attrs())
        super().__init__(attrs=attrs, choices=choices)


class TomSelect(TomSelectMixin, Select):
    """Render single choice fields with `TomSelect.js`."""


class TomSelectMultiple(TomSelectMixin, SelectMultiple):
    """Render multiple choice fields with `TomSelect.js`."""


class TomSelectLabel(TomSelectMixin, Select):
    """Render custom label choice fields."""

    ts_config = TomSelectConfig(is_label="true")


class TomSelectLabelMultiple(TomSelectMixin, SelectMultiple):
    """Render custom label fields with multiple choices possible."""

    ts_config = TomSelectConfig(is_label="true")


class EmptySelect(Select):
    def optgroups(self, name, value, attrs=None):
        """Render no full queryset options.

        Conditionally render only the currently selected value, so redisplay after
        validation errors still shows the selected item.
        """
        if not value:
            return []

        # value is usually a list of strings at widget-rendering time.
        selected_values = {str(v) for v in value if v not in self.choices.field.empty_values}

        if not selected_values:
            return []

        field = self.choices.field
        key = field.to_field_name or "pk"

        queryset = field.queryset.filter(**{f"{key}__in": selected_values})

        options = []
        for obj in queryset:
            option_value = field.prepare_value(obj)
            option_label = field.label_from_instance(obj)

            options.append(
                self.create_option(
                    name=name,
                    value=option_value,
                    label=option_label,
                    selected=str(option_value) in selected_values,
                    index=len(options),
                    attrs=attrs,
                )
            )

        return [(None, options, 0)]


class EmptySelectMultiple(EmptySelect):
    """Render no full queryset options.

    Conditionally render only the selected values, so redisplay after
    validation errors still shows the selected item.
    """

    allow_multiple_selected = True

    def value_from_datadict(self, data, files, name):
        try:
            getter = data.getlist
        except AttributeError:
            getter = data.get
        return getter(name)

    def value_omitted_from_data(self, data, files, name):
        return False


class ModelTomSelect(TomSelectMixin, EmptySelect):
    """Render single choice fields with `TomSelect.js`, using remote loading.

    This will *not* render any option by default, but rather relies on
    valid `url` configuration for loading data remotely.

    For example:

    ```
    class MyForm(forms.Form):
        my_field = TomSelectModelChoiceField(
            queryset=MyModel.objects.all(),
            widget=ModelTomSelect(
                ts_config=TomSelectConfig(
                    url=reverse_lazy("my_view"),
                    value_field="id",
                    label_field="name",
                    search_field=["name", "foofy"],
                )
            ),
        )
    ```

    `my_view` can be specified using `AutocompleteModelView`

    """


class ModelTomSelectMultiple(TomSelectMixin, EmptySelectMultiple):
    """Render multiple choice fields with `TomSelect.js`, using remote loading.

    For more information see the docstring of `ModelTomSelect`."""
