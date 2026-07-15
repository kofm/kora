import tomllib
from dataclasses import dataclass
from pathlib import Path

from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient, APITestCase

from collect.factories import SampleFactory, StoragePositionFactory
from describe.factories import (
    ExpressionFactory,
    ProtocolFactory,
    TraitFactory,
    WorkspaceElementFactory,
    WorkspaceFactory,
)
from register.factories import EntityFactory, PlantSpeciesFactory, PlantVarietyFactory, ProtectionFactory
from register.models import PlantVarietyName


@dataclass(frozen=True)
class ViewSpec:
    name: str
    fields: list[str]

    @property
    def url(self) -> str:
        return reverse(f"restapi:{self.name}")


def load_urls(path: Path) -> dict[str, ViewSpec]:
    with path.open("rb") as file:
        data = tomllib.load(file)["urls"]

    return {name: ViewSpec(name=name, fields=fields) for name, fields in data.items()}


class APITests(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username="testuser", password="testpass")
        self.client.login(username="testuser", password="testpass")

        self.species = PlantSpeciesFactory()
        self.variety = PlantVarietyFactory(species=self.species)
        self.breeder = EntityFactory(name="SeedCo")
        self.protection = ProtectionFactory(variety=self.variety)
        self.workspace = WorkspaceFactory(user=self.user, name="Test Workspace", is_active=True)
        self.workspace_element = WorkspaceElementFactory(workspace=self.workspace)
        ExpressionFactory.create_batch(3, description=self.workspace_element.description)
        SampleFactory(variety=self.variety)
        StoragePositionFactory()

        self.routes = load_urls(Path(__file__).with_name("urls.toml"))

    def test_views_smoke_test(self):
        for name, data in self.routes.items():
            response = self.client.get(data.url)
            self.assertEqual(response.status_code, status.HTTP_200_OK)
            self.assertIn("results", response.data)
            results = response.data["results"]
            self.assertTrue(
                isinstance(results, list),
                f"API view {name} response had returned unexpected type in `results` key.",
            )
            self.assertGreaterEqual(len(results), 1, f"API view {name} returned no results")
            self.assertEqual(
                set(data.fields),
                set(results[0].keys()),
                f"API view {name} returned unexpected shape of results",
            )

    def test_create_plant_variety(self):
        data = {"name": "Better Tomato", "species": self.species.pk}
        response = self.client.post(reverse("restapi:plantvariety-list"), data)
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
            }
            for name in names
        ]
        response = self.client.post(reverse("restapi:plantvariety-bulk"), data)
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

    def test_workspace_elements(self):
        response = self.client.get(
            reverse(
                "restapi:workspaceelements",
                kwargs={
                    "workspace": self.workspace.pk,
                },
            )
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("results", response.data)
        results = response.data["results"]
        self.assertEqual(len(results), 1)
        self.assertEqual(len(results[0]["description_detail"]["expressions"]), 3)

    def test_bulk_create_plant_species(self):
        species = (("Rye", "Secale cereale"), ("Rice", "Oryza sativa"))
        data = [
            {
                "common_name": common_name,
                "latin_name": latin_name,
                "plant_type": "herbaceous",
            }
            for common_name, latin_name in species
        ]
        response = self.client.post(reverse("restapi:plantspecies-bulk"), data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        common_names = [item["common_name"] for item in response.data]
        self.assertCountEqual(common_names, [item[0] for item in species])

    def test_bulk_create_entities(self):
        names = ("Mr. White", "MegaCorp")
        data = [{"name": name} for name in names]
        response = self.client.post(reverse("restapi:entities-bulk"), data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
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
        resp = self.client.post(reverse("restapi:protections-bulk"), data)
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
        resp = self.client.post(reverse("restapi:protocols-bulk"), data)
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)
        self.assertEqual(len(resp.data), 2)

    def test_bulk_create_trait(self):
        protocol = ProtocolFactory()
        data = [
            {"numeric_id": 1, "description": "Stem length", "protocol": protocol.pk},
            {"numeric_id": 2, "description": "Flowers colour", "protocol": protocol.pk},
        ]
        resp = self.client.post(reverse("restapi:traits-bulk"), data)
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
        resp = self.client.post(reverse("restapi:states-bulk"), data)
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)
        self.assertEqual(len(resp.data), 3)
