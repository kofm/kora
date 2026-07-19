from pathlib import Path

from django.contrib.auth.models import User
from django.core.files.uploadedfile import SimpleUploadedFile
from rest_framework.test import APIClient, APITestCase

from register.factories import PlantSpeciesFactory
from register.serializers import PlantVarietyImportRequestSerializer

FIXTURE_PATH = Path(__file__).parent / "fixtures"


class PlantVarietyImportTest(APITestCase):
    def setUp(self) -> None:
        self.client = APIClient()
        self.user = User.objects.create_user(username="testuser", password="testpass")
        self.client.login(username="testuser", password="testpass")
        self.species = PlantSpeciesFactory(id=1, common_name="Tomato")

    def get_serializer(self):
        return PlantVarietyImportRequestSerializer

    def test_plantvariety_import_serializer_succeeds(self):
        path = FIXTURE_PATH / "plantvarieties.xlsx"
        uploaded_file = SimpleUploadedFile(path.name, path.read_bytes())
        serializer = self.get_serializer()(data={"file": uploaded_file})

        self.assertTrue(serializer.is_valid(), serializer.errors)
        imported = serializer.save()

        self.assertSetEqual(
            {variety.name for variety in imported},
            {"Foobar", "Foofy", "Foofer"},
        )

    def test_plantvariety_import_serializer_rejects_unsupported_extension(self):
        text_file = SimpleUploadedFile(name="test.txt", content=b"species_id,name\n1,Antano\n")

        serializer = self.get_serializer()(data={"file": text_file})

        self.assertFalse(serializer.is_valid())
        self.assertIn("Supported file types", str(serializer.errors["file"]))
