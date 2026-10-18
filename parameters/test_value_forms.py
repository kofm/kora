from crispy_forms.utils import render_crispy_form
from django.template import Context, Template
from django.test import SimpleTestCase

from calculator.forms import ObservationParameterForm, ParameterTargetObservationForm
from parameters.forms import VarietyVarietalParameterForm
from parameters.models import Parameter


class TypedValueUnitTests(SimpleTestCase):
    def test_numeric_units_render_in_crispy_and_inline_forms(self):
        for kind in ("integer", "decimal"):
            with self.subTest(type=kind):
                parameter = Parameter(type=kind, measure_unit="g")
                form = VarietyVarietalParameterForm(parameter=parameter)
                form.fields["parameter"].queryset = Parameter.objects.none()
                inline = ParameterTargetObservationForm(parameter=parameter)
                for html in (
                    Template("{% load crispy_forms_tags %}{{ form|crispy }}").render(Context({"form": form})),
                    render_crispy_form(form),
                    str(inline.value_field),
                ):
                    self.assertIn('class="input-group"', html)
                    self.assertIn(f'<span class="input-group-text" id="id_value_{kind}_unit">g</span>', html)
                    self.assertIn('type="number"', html)
                self.assertIn('class="form-control form-control-lg"', str(inline.value_field))

    def test_only_numeric_parameters_with_units_get_addons(self):
        for parameter in (
            None,
            Parameter(type="integer", measure_unit=""),
            Parameter(type="decimal", measure_unit=""),
            *(Parameter(type=kind, measure_unit="g") for kind in ("boolean", "date", "text")),
        ):
            with self.subTest(parameter=parameter):
                form = ObservationParameterForm(parameter=parameter)
                self.assertNotIn("input-group", str(form.value_field))

    def test_unit_addon_preserves_descriptions_and_invalid_feedback(self):
        for prefix in ("first", "second"):
            with self.subTest(prefix=prefix):
                form = ObservationParameterForm(
                    data={f"{prefix}-value_decimal": "invalid"},
                    parameter=Parameter(type="decimal", measure_unit="<g>"),
                    prefix=prefix,
                )
                form.fields["parameter"].queryset = Parameter.objects.none()
                form.fields["value_decimal"].widget.attrs["aria-describedby"] = "value-help"
                # An invalid field must keep its feedback visible outside the input group.
                form.is_valid()
                html = Template("{% load crispy_forms_tags %}{{ form|crispy }}").render(Context({"form": form}))
                self.assertIn(f'aria-describedby="value-help id_{prefix}-value_decimal_unit"', html)
                self.assertIn(f'id="id_{prefix}-value_decimal_unit">&lt;g&gt;</span>', html)
                self.assertIn('class="input-group is-invalid"', html)
                self.assertIn("Enter a number.", html)


class TypedValuePlaceholderTests(SimpleTestCase):
    def test_unselected_parameter_has_disabled_placeholder_after_selector(self):
        for form_class in (ObservationParameterForm, VarietyVarietalParameterForm):
            with self.subTest(form=form_class.__name__):
                form = form_class()
                field = form.fields["value_placeholder"]
                self.assertTrue(field.disabled)
                self.assertFalse(field.required)
                self.assertEqual(field.label, "Value")
                fields = list(form.fields)
                self.assertEqual(fields.index("value_placeholder"), fields.index("parameter") + 1)
                self.assertEqual(form.value_field.name, "value_placeholder")
                self.assertIn("Select a parameter first", str(form.value_field))
                self.assertIn("disabled", str(form.value_field))

    def test_refresh_targets_only_value_wrapper(self):
        for parameter in (None, Parameter(type="integer")):
            with self.subTest(parameter=parameter):
                form = ObservationParameterForm(parameter=parameter, parameter_refresh_url="/observations/new/")
                form.fields["parameter"].queryset = Parameter.objects.none()
                attrs = form.fields["parameter"].widget.attrs
                self.assertEqual(attrs["hx-target"], "next .typed-value-field")
                self.assertEqual(attrs["hx-select"], "form:has([name='parameter']) .typed-value-field")
                # Modal forms use the crispy filter; other pages use the crispy tag.
                for html in (
                    Template("{% load crispy_forms_tags %}{{ form|crispy }}").render(Context({"form": form})),
                    render_crispy_form(form),
                ):
                    self.assertIn('class="mb-3 typed-value-field"', html)
                    self.assertEqual(html.count('class="mb-3 typed-value-field"'), 1)

    def test_selected_parameter_replaces_placeholder_with_typed_field(self):
        for kind in Parameter.Type.values:
            with self.subTest(type=kind):
                form = ObservationParameterForm(parameter=Parameter(type=kind))
                self.assertNotIn("value_placeholder", form.fields)
                self.assertEqual(form.value_field.name, f"value_{kind}")
                self.assertTrue(form.value_field.field.required)
                self.assertFalse(form.value_field.field.disabled)
