from django.test import TestCase
from django.urls import reverse

from frontpage.factories import UserFactory
from parameters.factories import ParameterFactory
from parameters.forms import VarietalParameterForm
from register.factories import PlantSpeciesFactory, PlantVarietyFactory


class ParameterAutocompleteTests(TestCase):
    def test_searches_code_and_name_with_deterministic_order(self):
        self.client.force_login(UserFactory())
        first = ParameterFactory(code="ALPHA", name="Stem length")
        second = ParameterFactory(code="STEM_B", name="Plant height")
        ParameterFactory(code="LEAF_A", name="Leaf width")

        response = self.client.get(reverse("parameters:parameter_autocomplete"), {"q": "stem"})

        self.assertEqual(
            [result["id"] for result in response.json()["results"]],
            [first.pk, second.pk],
        )


class VarietalParameterFormTests(TestCase):
    def test_rejects_variety_from_different_species(self):
        selected_species = PlantSpeciesFactory()
        variety = PlantVarietyFactory()
        parameter = ParameterFactory()

        form = VarietalParameterForm(
            data={
                "species": selected_species.pk,
                "variety": variety.pk,
                "parameter": parameter.pk,
                "value": 1,
            }
        )

        self.assertFalse(form.is_valid())
        self.assertIn("variety", form.errors)
