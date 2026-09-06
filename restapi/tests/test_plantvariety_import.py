from pathlib import Path

from django.contrib.auth.models import Permission, User
from django.core.files.uploadedfile import SimpleUploadedFile
from django.urls import reverse
from rest_framework.test import APIClient, APITestCase

from register.factories import PlantSpeciesFactory, PlantVarietyFactory
from register.models import PlantVariety, PlantVarietyName
from register.serializers import PlantVarietyImportRequestSerializer

FIXTURE_PATH = Path(__file__).parent / "fixtures"


class PlantVarietyImportTest(APITestCase):
    def setUp(self) -> None:
        self.client = APIClient()
        self.user = User.objects.create_user(username="testuser", password="testpass")
        self.user.user_permissions.add(
            *[
                Permission.objects.get(codename=codename)
                for codename in ("add_plantvariety", "add_plantvarietyname")
            ]
        )
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

    def test_import_skips_trimmed_existing_variety_and_creates_trimmed_new_variety(self):
        PlantVarietyFactory(name="Foobar", species=self.species)
        uploaded_file = SimpleUploadedFile(
            name="varieties.csv",
            content=b"species_id,name\n1,  Foobar  \n1,  New variety  \n",
            content_type="text/csv",
        )

        response = self.client.post(
            reverse("restapi:plantvariety-excel-import"),
            {"file": uploaded_file},
            format="multipart",
        )

        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json(), {"imported_rows": 1})
        self.assertSetEqual(
            set(PlantVariety.objects.values_list("name", flat=True)),
            {"Foobar", "New variety"},
        )
        new_variety = PlantVariety.objects.get(name="New variety", species=self.species)
        self.assertTrue(PlantVarietyName.objects.filter(variety=new_variety, name="New variety").exists())
