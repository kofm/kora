from pathlib import Path

from django.core.files.uploadedfile import SimpleUploadedFile
from factory.declarations import Iterator
from rest_framework.test import APITestCase

from register.factories import EntityFactory, PlantSpeciesFactory, PlantVarietyFactory
from register.models import Protection, ProtectionType
from register.serializers import ProtectionImportRequestSerializer, ProtectionImportRowSerializer

FIXTURE_PATH = Path(__file__).parent / "fixtures"


class ProtectionExcelImportTest(APITestCase):
    def setUp(self):
        self.species = PlantSpeciesFactory(id=1)
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

        serializer = ProtectionImportRowSerializer(data=data, many=True)

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
        path = FIXTURE_PATH / "protections.xlsx"
        uploaded_file = SimpleUploadedFile(path.name, path.read_bytes())
        s = ProtectionImportRequestSerializer(data={"file": uploaded_file})
        self.assertTrue(s.is_valid())

        res = s.save()
        self.assertEqual(len(res), 2)
        self.assertEqual(res[0][0].variety, varieties[0])
        self.assertEqual(res[1][0].variety, varieties[1])
        # It created 2 Entities
        self.assertEqual(len(res[0][1]), 2)
        self.assertEqual(res[0][1][0], entities[0])
        self.assertEqual(res[0][1][1], entities[1])
