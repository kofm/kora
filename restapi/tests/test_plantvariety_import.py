from django.contrib.auth.models import User
from rest_framework.test import APIClient, APITestCase

from register.factories import PlantSpeciesFactory
from register.serializers import PlantVarietyImportSerializer
from restapi.tests.utils import make_excel_file


class PlantVarietyImportTest(APITestCase):
    def setUp(self) -> None:
        self.client = APIClient()
        self.user = User.objects.create_user(username="testuser", password="testpass")
        self.client.login(username="testuser", password="testpass")
        self.species = PlantSpeciesFactory(common_name="Tomato")

        data = [
            {"species_id": self.species.pk, "name": "Antano"},
            {"species_id": self.species.pk, "name": "Seccagno"},
        ]
        self.file = make_excel_file(data)

    def get_serializer(self):
        return PlantVarietyImportSerializer

    def test_plantvariety_import_serializer_succeed(self):
        sr = self.get_serializer()(data={"file": self.file})
        self.assertTrue(sr.is_valid())
        objs = sr.save()
        self.assertEqual(len(objs), 2)

    # def test_plantvariety_import_serializer_fails_with_missing_data(self):
    #     data = [
    #         {"species_id": self.species.pk, "name": ""},
    #         {"species_id": self.species.pk, "name": "Seccagno"},
    #     ]
    #     sr = self.get_serializer()(data={"file": make_excel_file(data)})
