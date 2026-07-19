from pathlib import Path

from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase

from register.factories import PlantSpeciesFactory
from register.serializers import PlantVarietyImportRequestSerializer

FIXTURE_PATH = Path(__file__).parent / "fixtures"


class SpreadsheetImportTest(TestCase):
    filenames = (
        "plantvarieties.xlsx",
        "plantvarieties.xls",
        "plantvarieties.ods",
        "plantvarieties.csv",
    )

    def setUp(self):
        PlantSpeciesFactory(id=1)

    def test_import_supported_formats(self):
        for filename in self.filenames:
            with self.subTest(filename=filename):
                path = FIXTURE_PATH / filename
                uploaded_file = SimpleUploadedFile(path.name, path.read_bytes())
                serializer = PlantVarietyImportRequestSerializer(data={"file": uploaded_file})

                self.assertTrue(serializer.is_valid(), serializer.errors)
                imported = serializer.save()

                self.assertSetEqual(
                    {variety.name for variety in imported},
                    {"Foobar", "Foofy", "Foofer"},
                )
                self.assertTrue(all(variety.species_id == 1 for variety in imported))
