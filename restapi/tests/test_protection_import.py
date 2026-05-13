from factory.declarations import Iterator
from rest_framework.test import APITestCase

from register.factories import EntityFactory, PlantSpeciesFactory, PlantVarietyFactory
from register.models import Protection, ProtectionType
from register.serializers import ProtectionExcelImportSerializer, ProtectionRowSerializer
from restapi.tests.utils import make_excel_file


class ProtectionExcelImportTest(APITestCase):
    def setUp(self):
        self.species = PlantSpeciesFactory()
        self.variety = PlantVarietyFactory(species=self.species)

    def test_existing_protection_is_deduplicated_when_type_is_imported_by_code(self):
        nli = ProtectionType.objects.get(code="NLI")

        Protection.objects.create(
            type=nli,
            variety=self.variety,
            country="IT",
            status="G",
            reference="existing",
        )

        data = [
            {
                "type": "NLI",
                "country": "IT",
                "name": self.variety.name,
                "species_id": self.variety.species_id,
                "reference": "should not create duplicate",
                "status": "W",
            }
        ]

        serializer = ProtectionRowSerializer(data=data, many=True)

        self.assertTrue(serializer.is_valid(), serializer.errors)

        objs = serializer.save()

        self.assertEqual(len(objs), 1)

        obj, applicants, maintainers = objs[0]

        self.assertIsNone(obj)
        self.assertEqual(applicants, [])
        self.assertEqual(maintainers, [])

    def test_serializer_import_succeed(self):
        varieties = PlantVarietyFactory.create_batch(2, name=Iterator(["Carnaroli", "Foo"]), species=self.species)
        entities = EntityFactory.create_batch(2, name=Iterator(["Bar", "Baz"]))
        data = [
            {
                "type": "NLI",
                "reference": "abcde",
                "status": "G",
                "country": "IT",
                "name": "Carnaroli",
                "species_id": self.species.pk,
                "date_start": "2024-02-02",
                "date_end": "",
                "applicants": "Bar; Baz",
                "maintainers": "Bar",
                "note": "My note",
            },
            {
                "type": "PBR",
                "reference": "fght",
                "status": "W",
                "country": "ES",
                "name": "Foo",
                "species_id": self.species.pk,
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
