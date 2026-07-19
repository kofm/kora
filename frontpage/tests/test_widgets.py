from django import forms
from django.test import TestCase

from frontpage.widgets import EmptySelect, TomSelect, TomSelectConfig
from register.factories import PlantVarietyFactory
from register.models import PlantSpecies, PlantVariety


class TestModelForm(forms.ModelForm):
    class Meta:
        model = PlantVariety
        fields = ["species"]
        widgets = {"species": EmptySelect()}


class TomSelectForm(forms.Form):
    my_field = forms.ChoiceField(
        choices=[(1, "foo"), (2, "bar")],
        widget=TomSelect(ts_config=TomSelectConfig(url="/foofy")),
    )


class EmptySelectTest(TestCase):
    def setUp(self) -> None:
        PlantVarietyFactory.create_batch(4)

        class TestForm(forms.Form):
            species = forms.ModelChoiceField(queryset=PlantSpecies.objects.all(), widget=EmptySelect())

        self.form = TestForm()

    def test_empty_select_renders_no_options(self):
        self.assertTrue(PlantSpecies.objects.exists())  # prove data exists

        html = self.form["species"].as_widget()

        self.assertIn("<select", html)
        self.assertNotIn("<option", html)

    def test_empty_select_renders_initial_options_in_modelform(self):
        instance = PlantVariety.objects.first()
        form = TestModelForm(instance=instance)
        html = form["species"].as_widget()

        self.assertIn("<select", html)
        self.assertEqual(html.count("<option"), 1)

        self.assertInHTML(
            f'<option value="{instance.species_id}" selected>{instance.species}</option>',
            html,
        )


class TomSelectTest(TestCase):
    def setUp(self) -> None:
        pass

    def test_tomselect_config_returns_kebab_cased_and_prefixed_default_config(self):
        ts_config = TomSelectConfig()
        attrs = ts_config.attrs()
        self.assertIn("data-ts-max-options", attrs)
        self.assertIn("data-ts-preload", attrs)

    def test_tomselect_config_returns_kebab_cased_and_prefixed_config(self):
        ts_config = TomSelectConfig(
            url="/search",
            value_field="id",
            label_field="name",
        )
        attrs = ts_config.attrs()

        self.assertIn("data-ts-url", attrs)
        self.assertIn("data-ts-value-field", attrs)
        self.assertIn("data-ts-label-field", attrs)

        self.assertEqual(attrs["data-ts-url"], "/search")
        self.assertEqual(attrs["data-ts-value-field"], "id")
        self.assertEqual(attrs["data-ts-label-field"], "name")

    def test_tomselect_config_returns_kebab_cased_valid_json_list(self):
        ts_config = TomSelectConfig(search_field=["foo", "bar"])
        attrs = ts_config.attrs()

        self.assertIn("data-ts-search-field", attrs)
        self.assertEqual(attrs["data-ts-search-field"], '["foo", "bar"]')

    def test_tomselect_mixin_is_applying_tomselect_class_to_the_widget(self):
        form = TomSelectForm()
        widget_attrs = form.fields["my_field"].widget.attrs
        self.assertIn("class", widget_attrs)
        self.assertIn("tomselect", widget_attrs["class"].split())

    def test_tomselect_config_is_merged_into_field_attrs(self):
        form = TomSelectForm()
        widget_attrs = form.fields["my_field"].widget.attrs
        self.assertIn("data-ts-url", widget_attrs)
