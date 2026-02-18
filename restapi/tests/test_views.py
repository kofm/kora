from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient, APITestCase

from describe.factories import (
    ExpressionFactory,
    ProtocolFactory,
    TraitFactory,
    WorkspaceElementFactory,
    WorkspaceFactory,
)
from register.factories import EntityFactory, PlantSpeciesFactory, PlantVarietyFactory
from register.models import PlantVarietyName


class APITests(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username="testuser", password="testpass")
        self.client.login(username="testuser", password="testpass")

        self.species = PlantSpeciesFactory()
        self.breeder = EntityFactory(name="SeedCo")

        self.plantspecies_list_url = reverse("restapi:plantspecies-list")
        self.plantvariety_list_url = reverse("restapi:plantvariety-list")
        self.entity_list_url = reverse("restapi:entity-list")
        self.protection_list_url = reverse("restapi:protection-list")

    def test_list_plant_species(self):
        response = self.client.get(self.plantspecies_list_url, {"no_pagination": 1})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(any(d["common_name"] == self.species.common_name for d in response.data))

    def test_create_plant_variety(self):
        data = {
            "name": "Better Tomato",
            "species": self.species.pk,
            "breeder": self.breeder.pk,
        }
        response = self.client.post(self.plantvariety_list_url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["name"], "Better Tomato")
        self.assertEqual(response.data["species"], self.species.pk)

        variety_id = response.data["id"]
        denomination_exists = PlantVarietyName.objects.filter(variety__pk=variety_id, name="Better Tomato").exists()
        self.assertTrue(denomination_exists)

    def test_bulk_create_plant_variety(self):
        names = ["Better Tomato", "Another Better Tomato"]
        data = [
            {
                "name": name,
                "species": self.species.pk,
                "breeder": self.breeder.pk,
            }
            for name in names
        ]
        response = self.client.post(self.plantvariety_list_url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        variety_ids = [item["id"] for item in response.data]
        variety_names = PlantVarietyName.objects.filter(variety__in=variety_ids)
        self.assertEqual(len(response.data), 2)
        self.assertEqual(len(variety_names), 2)
        self.assertEqual(list(variety_names.values_list("name", flat=True)), names)

    def test_retrieve_plant_variety(self):
        variety = PlantVarietyFactory(name="Golden Apple", species=self.species)
        url = reverse("restapi:plantvariety-detail", args=[variety.pk])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["name"], variety.name)
        self.assertEqual(response.data["species"], variety.species.pk)

    def test_list_entities(self):
        response = self.client.get(self.entity_list_url + "?no_pagination=1")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(any(d["name"] == self.breeder.name for d in response.data))

    def test_workspace_elements(self):
        workspace = WorkspaceFactory(user=self.user, name="Test Workspace", is_active=True)
        workspace_element = WorkspaceElementFactory(workspace=workspace)
        ExpressionFactory.create_batch(3, description=workspace_element.description)
        response = self.client.get(reverse("restapi:workspace_elements", args=(workspace.pk,)), {"no_pagination": 1})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(len(response.data[0]["description"]["expressions"]), 3)

    def test_bulk_create_plant_species(self):
        species = (("Tomato", "Solanum lycopersicon"), ("Rice", "Oryza sativa"))
        data = [
            {
                "common_name": common_name,
                "latin_name": latin_name,
                "plant_type": "herbaceous",
            }
            for common_name, latin_name in species
        ]
        response = self.client.post(self.plantspecies_list_url, data)
        self.assertEqual(
            response.status_code, status.HTTP_201_CREATED, f"Expected 201, got {response.status_code}: {response.data}"
        )
        common_names = [item["common_name"] for item in response.data]
        self.assertCountEqual(common_names, [item[0] for item in species])

    def test_bulk_create_entities(self):
        names = ("Mr. White", "MegaCorp")
        data = [{"name": name} for name in names]
        response = self.client.post(self.entity_list_url, data)
        self.assertEqual(
            response.status_code, status.HTTP_201_CREATED, f"Expected 201, got {response.status_code}: {response.data}"
        )
        returned_names = [item["name"] for item in response.data]
        self.assertCountEqual(returned_names, names)

    def test_bulk_create_protections(self):
        varieties = PlantVarietyFactory.create_batch(2)
        data = [
            {
                "type": "NLI",
                "reference": "456fff",
                "status": "W",
                "country": "GR",
                "variety": varieties[1].pk,
                "date_start": "2023-12-11",
            },
            {
                "type": "NLI",
                "reference": "123abc",
                "status": "G",
                "country": "IT",
                "variety": varieties[0].pk,
                "date_start": "2024-01-01",
            },
        ]
        resp = self.client.post(reverse("restapi:protection-list"), data)
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)
        self.assertEqual(len(resp.data), 2)

    def test_bulk_create_protocol(self):
        data = [
            {
                "name": "TP123",
                "plantspecies": self.species.pk,
                "url_ref": "http://example.com",
            },
            {
                "name": "TP456",
                "plantspecies": self.species.pk,
                "url_ref": "http://example.com",
            },
        ]
        resp = self.client.post(reverse("restapi:protocols-list"), data)
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)
        self.assertEqual(len(resp.data), 2)

    def test_bulk_create_trait(self):
        protocol = ProtocolFactory()
        data = [
            {"numeric_id": 1, "description": "Stem length", "protocol": protocol.pk},
            {"numeric_id": 2, "description": "Flowers colour", "protocol": protocol.pk},
        ]
        resp = self.client.post(reverse("restapi:traits-list"), data)
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)
        self.assertEqual(len(resp.data), 2)

    def test_bulk_create_state(self):
        trait = TraitFactory()
        data = [
            {
                "numeric_id": 3,
                "description": "light",
                "trait": trait.pk,
            },
            {
                "numeric_id": 5,
                "description": "medium",
                "trait": trait.pk,
            },
            {
                "numeric_id": 7,
                "description": "dark",
                "trait": trait.pk,
            },
        ]
        resp = self.client.post(reverse("restapi:states-list"), data)
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)
        self.assertEqual(len(resp.data), 3)
