from django.test import TestCase

from describe.factories import ExpressionFactory
from describe.forms import DescriptionUpdateForm, ExpressionForm, TraitForm


class InlineFormRenderingTests(TestCase):
    def test_inline_fields_preserve_bootstrap_and_validation_feedback(self):
        expression = ExpressionFactory()
        trait = expression.state.trait
        cases = (
            (
                ExpressionForm,
                expression,
                {"description": expression.description_id, "state": expression.state_id, "note": "Notes"},
                "state",
                "form-select",
                False,
            ),
            (
                DescriptionUpdateForm,
                expression.description,
                {"label": expression.description.label_id, "notes": "Notes"},
                "label",
                "form-select",
                False,
            ),
            (
                TraitForm,
                trait,
                {
                    "numeric_id": trait.numeric_id,
                    "description": trait.description,
                    "type_of_expression": trait.type_of_expression,
                    "protocol": trait.protocol_id,
                },
                "numeric_id",
                "form-control",
                True,
            ),
        )
        for form_class, instance, valid_data, field_name, base_class, show_errors in cases:
            for state in ("unbound", "valid", "invalid"):
                with self.subTest(form=form_class.__name__, state=state):
                    data = None if state == "unbound" else dict(valid_data)
                    if state == "invalid":
                        data[field_name] = ""
                    form = form_class(data=data, instance=instance)
                    if isinstance(form, ExpressionForm):
                        form.fields["state"].queryset = trait.states.all()
                    if state != "unbound":
                        self.assertEqual(form.is_valid(), state == "valid", form.errors)
                    html = str(form[field_name])
                    self.assertIn(base_class, html)
                    self.assertEqual("is-valid" in html, state == "valid")
                    self.assertEqual("is-invalid" in html, state == "invalid" and show_errors)
                    if isinstance(form, DescriptionUpdateForm):
                        self.assertIn("tomselect", html)
