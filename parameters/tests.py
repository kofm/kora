from django.test import TestCase
from django.urls import reverse

from frontpage.factories import UserFactory
from parameters.factories import ParameterFactory
from parameters.forms import VarietalParameterForm, VarietyVarietalParameterForm
from parameters.models import VarietalParameter
from register.factories import PlantSpeciesFactory, PlantVarietyFactory


class ParameterAutocompleteTests(TestCase):
    def test_searches_code_and_name_with_deterministic_order(self):
        self.client.force_login(UserFactory())
        first = ParameterFactory(code="ALPHA", name="Stem length", measure_unit="cm")
        second = ParameterFactory(code="STEM_B", name="Plant height", measure_unit="")
        ParameterFactory(code="LEAF_A", name="Leaf width")

        response = self.client.get(reverse("parameters:parameter_autocomplete"), {"q": "stem"})

        self.assertEqual(
            [result["id"] for result in response.json()["results"]],
            [first.pk, second.pk],
        )
        self.assertEqual(
            [result["text"] for result in response.json()["results"]],
            ["Stem length", "Plant height"],
        )
        for parameter in (first, second):
            form = VarietyVarietalParameterForm(initial={"parameter": parameter.pk})
            self.assertInHTML(
                f'<option value="{parameter.pk}" selected>{parameter.name}</option>',
                str(form["parameter"]),
            )


class VarietalParameterFormTests(TestCase):
    def test_parameter_selection_refresh_preserves_context_and_accepts_false(self):
        self.client.force_login(UserFactory(is_superuser=True))
        variety = PlantVarietyFactory()
        parameter = ParameterFactory(type="boolean")
        url = reverse("parameters:varietalparameter_create")
        data = {
            "species": variety.species_id,
            "variety": variety.pk,
            "parameter": parameter.pk,
            "note": "Literature reference",
            "url_ref": "https://example.com/source",
        }
        refreshed = self.client.get(url, data, HTTP_HX_REQUEST="true")
        self.assertEqual(refreshed.status_code, 200)
        self.assertContains(refreshed, f'hx-get="{url}')
        self.assertContains(refreshed, 'name="value_boolean"')
        self.assertContains(refreshed, "Literature reference")
        self.assertContains(refreshed, "https://example.com/source")
        saved = self.client.post(url, {**data, "value_boolean": "False"}, HTTP_HX_REQUEST="true")
        self.assertEqual(saved.status_code, 200)
        reference = VarietalParameter.objects.get(parameter=parameter, variety=variety)
        self.assertIs(reference.value_boolean, False)
        self.assertEqual(reference.note, data["note"])
        self.assertEqual(reference.url_ref, data["url_ref"])

    def test_update_preserves_parameter_despite_query_and_post_overrides(self):
        self.client.force_login(UserFactory(is_superuser=True))
        reference = VarietalParameter.objects.create(
            variety=PlantVarietyFactory(), parameter=ParameterFactory(type="integer"), value_integer=1
        )
        other = ParameterFactory(type="text")
        url = reverse("parameters:varietalparameter_update", args=[reference.pk])
        response = self.client.get(url, {"parameter": other.pk})
        self.assertContains(response, 'name="value_integer"')
        response = self.client.post(
            f"{url}?parameter={other.pk}",
            {"parameter": other.pk, "value_integer": "2", "note": "Corrected value"},
        )
        self.assertEqual(response.status_code, 302)
        original_parameter_id = reference.parameter_id
        reference.refresh_from_db()
        self.assertEqual(reference.parameter_id, original_parameter_id)
        self.assertEqual(reference.value_integer, 2)
        self.assertEqual(reference.note, "Corrected value")

    def test_modal_mutations_refresh_value_tables(self):
        self.client.force_login(UserFactory(is_superuser=True))
        for action in ("update", "delete"):
            with self.subTest(action=action):
                reference = VarietalParameter.objects.create(
                    variety=PlantVarietyFactory(), parameter=ParameterFactory(type="integer"), value_integer=1
                )
                url = reverse(f"parameters:varietalparameter_{action}", args=[reference.pk])
                response = self.client.post(
                    url,
                    {"value_integer": "2"},
                    HTTP_HX_REQUEST="true",
                )
                self.assertEqual(response.status_code, 200)
                self.assertJSONEqual(
                    response.headers["HX-Trigger"],
                    {"closeModal": True, "resultsChanged": True, "varietalParametersChanged": True},
                )
                if action == "update":
                    reference.refresh_from_db()
                    self.assertEqual(reference.value_integer, 2)
                else:
                    self.assertFalse(VarietalParameter.objects.filter(pk=reference.pk).exists())

    def test_rejects_variety_from_different_species(self):
        selected_species = PlantSpeciesFactory()
        variety = PlantVarietyFactory()
        parameter = ParameterFactory()

        form = VarietalParameterForm(
            data={
                "species": selected_species.pk,
                "variety": variety.pk,
                "parameter": parameter.pk,
                "value_decimal": 1,
            }
        )

        self.assertFalse(form.is_valid())
        self.assertIn("variety", form.errors)
