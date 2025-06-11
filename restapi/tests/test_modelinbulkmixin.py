from rest_framework.test import APITestCase

from register.factories import PlantSpeciesFactory, PlantVarietyFactory
from register.models import PlantVariety
from register.serializers import ModelInBulkMixin


class ModelInBulkMixinTest(APITestCase):
    def setUp(self) -> None:
        self.species = PlantSpeciesFactory(common_name="Tomato")

        self.vantano = PlantVarietyFactory(name="Antano", species=self.species)
        self.vseccagno = PlantVarietyFactory(name="Seccagno", species=self.species)

        self.data = [
            {"species_id": self.species.pk, "name": "Antano"},
            {"species_id": self.species.pk, "name": "Seccagno"},
        ]

    def test_to_mapping_method_create_mapping(self):
        mod = ModelInBulkMixin
        result = mod.to_mapping(
            queryset=PlantVariety.objects.all(), lookup_fields=["name", "species_id"], data=self.data
        )
        self.assertIn(("Antano", self.species.pk), result)
        self.assertIn(("Seccagno", self.species.pk), result)
        self.assertEqual(result[("Antano", self.species.pk)].name, "Antano")
        self.assertEqual(result[("Antano", self.species.pk)].species, self.species)

        self.assertEqual(result[("Seccagno", self.species.pk)].name, "Seccagno")
        self.assertEqual(result[("Seccagno", self.species.pk)].species, self.species)
