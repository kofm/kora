from factory.declarations import Iterator
from rest_framework.test import APITestCase

from register.factories import EntityFactory, PlantSpeciesFactory, PlantVarietyFactory
from register.serializers import ProtectionExcelImportSerializer
from restapi.tests.utils import make_excel_file


class ProtectionExcelImportTest(APITestCase):
    def setUp(self) -> None:
        pass

    def test_serializer_import_succeed(self):
        species = PlantSpeciesFactory()
        varieties = PlantVarietyFactory.create_batch(2, name=Iterator(["Carnaroli", "Foo"]), species=species)
        entities = EntityFactory.create_batch(2, name=Iterator(["Bar", "Baz"]))
        data = [
            {
                "type": "NLI",
                "reference": "abcde",
                "status": "G",
                "country": "IT",
                "name": "Carnaroli",
                "species_id": species.pk,
                "date_start": "2024-02-02",
                "date_end": "",
                "applicants": "Bar; Baz",
                "maintainers": "Bar",
                "note": "My note",
            },
            {
                "type": "NLI",
                "reference": "fght",
                "status": "W",
                "country": "ES",
                "name": "Foo",
                "species_id": species.pk,
                "date_start": "2024-02-01",
                "date_end": None,
                "applicants": "Bar",
                "maintainers": "Baz",
                "note": "",
            },
        ]
        file = make_excel_file(data)
        s = ProtectionExcelImportSerializer(data={"file": file})
        self.assertTrue(s.is_valid())

        res = s.save()
        self.assertEqual(len(res), 2)
        self.assertEqual(res[0][0].variety, varieties[0])
        self.assertEqual(res[1][0].variety, varieties[1])
        # It created 2 Entities
        self.assertEqual(len(res[0][1]), 2)
        self.assertEqual(res[0][1][0], entities[0])
        self.assertEqual(res[0][1][1], entities[1])
