import json
import tomllib
from dataclasses import dataclass
from pathlib import Path

from django.contrib.auth.models import Permission, User
from django.core.files.uploadedfile import SimpleUploadedFile
from django.urls import reverse
from django.utils import timezone
from rest_framework import status
from rest_framework.test import APIClient, APITestCase

from calculator.factories import (
    CropFactory,
    CropLayoutFactory,
    FieldBookFactory,
    ParameterObservationFactory,
    StepFactory,
    TraitObservationFactory,
)
from calculator.models import Crop, ParameterTarget, TraitObservation
from collect.factories import SampleFactory, StoragePositionFactory
from describe.factories import (
    ExpressionFactory,
    ProtocolFactory,
    StateFactory,
    TraitFactory,
    WorkspaceElementFactory,
    WorkspaceFactory,
)
from parameters.factories import ParameterFactory
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
        self.user.user_permissions.add(
            Permission.objects.get(codename="view_crop"),
            Permission.objects.get(codename="view_croplayout"),
            Permission.objects.get(codename="view_traitobservation"),
            Permission.objects.get(codename="view_parameterobservation"),
        )
        self.client.login(username="testuser", password="testpass")

        self.species = PlantSpeciesFactory()
        self.variety = PlantVarietyFactory(species=self.species)
        self.breeder = EntityFactory(name="SeedCo")
        self.protection = ProtectionFactory(variety=self.variety)
        self.workspace = WorkspaceFactory(user=self.user, name="Test Workspace", is_active=True)
        self.workspace_element = WorkspaceElementFactory(workspace=self.workspace)
        self.crop = CropFactory(variety=self.variety)
        TraitObservationFactory(crop=self.crop, created_by=self.user)
        ParameterObservationFactory(crop=self.crop, created_by=self.user)
        ExpressionFactory.create_batch(3, description=self.workspace_element.description)
        SampleFactory(variety=self.variety)
        StoragePositionFactory()

        self.routes = load_urls(Path(__file__).with_name("urls.toml"))

    def test_views_smoke_test(self):
        for name, data in self.routes.items():
            response = self.client.get(data.url)
            self.assertEqual(response.status_code, status.HTTP_200_OK, f"Failing view {data.url}")
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


class CalculatorAPIPermissionTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="calculator-api-user", password="testpass")
        self.client.force_authenticate(self.user)
        self.layout = CropLayoutFactory(name="Existing layout")
        self.crop = CropFactory(layout=self.layout, notes="Existing notes")

    def test_actions_require_corresponding_model_permissions(self):
        requests = (
            ("get", "crop-layout", self.layout, None),
            ("post", "crop-layout", None, {"name": "Unauthorized layout"}),
            ("patch", "crop-layout", self.layout, {"name": "Unauthorized update"}),
            ("delete", "crop-layout", self.layout, None),
            ("get", "crops", self.crop, None),
            ("post", "crops", None, {"layout": self.layout.pk, "variety": self.crop.variety_id}),
            ("patch", "crops", self.crop, {"notes": "Unauthorized update"}),
            ("delete", "crops", self.crop, None),
        )
        original_crop_notes = self.crop.notes

        for method, route_name, instance, payload in requests:
            with self.subTest(method=method, route_name=route_name):
                if instance is None:
                    url = reverse(f"restapi:{route_name}-list")
                else:
                    url = reverse(f"restapi:{route_name}-detail", args=[instance.pk])
                response = getattr(self.client, method)(url, payload or {})

                self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        self.crop.refresh_from_db()
        self.assertEqual(self.crop.notes, original_crop_notes)

    def test_crop_update_allows_only_varieties_from_the_existing_species(self):
        self.user.user_permissions.add(Permission.objects.get(codename="change_crop"))
        same_species_variety = PlantVarietyFactory(species=self.crop.variety.species)
        update_url = reverse("restapi:crops-detail", args=[self.crop.pk])

        response = self.client.patch(update_url, {"variety": same_species_variety.pk})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.crop.refresh_from_db()
        self.assertEqual(self.crop.variety, same_species_variety)

        other_species = PlantSpeciesFactory(common_name="Rice", latin_name="Oryza sativa")
        other_species_variety = PlantVarietyFactory(species=other_species)
        response = self.client.patch(update_url, {"variety": other_species_variety.pk})

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("variety", response.data)
        self.crop.refresh_from_db()
        self.assertEqual(self.crop.variety, same_species_variety)


class CropAPIUpdateTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="crop-api-user", password="testpass")
        self.client.force_authenticate(self.user)
        self.layout = CropLayoutFactory(name="Existing layout")
        self.crop = CropFactory(layout=self.layout, notes="Existing notes")
        self.update_url = reverse("restapi:crops-detail", args=[self.crop.pk])

    def test_crop_creation_accepts_layout(self):
        self.user.user_permissions.add(Permission.objects.get(codename="add_crop"))
        layout = CropLayoutFactory(name="New crop layout")
        variety = PlantVarietyFactory()

        response = self.client.post(
            reverse("restapi:crops-list"),
            {"layout": layout.pk, "variety": variety.pk, "notes": "Created through API"},
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(Crop.objects.filter(layout=layout, variety=variety, notes="Created through API").exists())

    def test_crop_without_steps_cannot_change_layout(self):
        self.user.user_permissions.add(Permission.objects.get(codename="change_crop"))
        other_layout = CropLayoutFactory(name="Other layout")

        response = self.client.patch(self.update_url, {"layout": other_layout.pk})

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data["layout"], ["The crop layout cannot be changed."])
        self.crop.refresh_from_db()
        self.assertEqual(self.crop.layout, self.layout)

    def test_rejected_layout_change_preserves_field_book_data(self):
        self.user.user_permissions.add(Permission.objects.get(codename="change_crop"))
        fieldbook = FieldBookFactory(layout=self.layout)
        step = StepFactory(fieldbook=fieldbook, crop=self.crop)
        parameter = ParameterFactory()
        target = ParameterTarget.objects.create(step=step, parameter=parameter)
        observation = ParameterObservationFactory(
            crop=self.crop,
            step=step,
            parameter=parameter,
            created_by=self.user,
        )
        other_layout = CropLayoutFactory(name="Other layout")

        response = self.client.patch(self.update_url, {"layout": other_layout.pk})

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.crop.refresh_from_db()
        step.refresh_from_db()
        target.refresh_from_db()
        observation.refresh_from_db()
        self.assertEqual(self.crop.layout, self.layout)
        self.assertEqual(step.fieldbook, fieldbook)
        self.assertEqual(step.crop, self.crop)
        self.assertEqual(target.step, step)
        self.assertEqual(observation.step, step)
        self.assertEqual(observation.crop, self.crop)

    def test_crop_update_accepts_existing_layout(self):
        self.user.user_permissions.add(Permission.objects.get(codename="change_crop"))

        response = self.client.patch(self.update_url, {"layout": self.layout.pk, "notes": "Updated notes"})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.crop.refresh_from_db()
        self.assertEqual(self.crop.layout, self.layout)
        self.assertEqual(self.crop.notes, "Updated notes")

    def test_partial_crop_update_can_omit_layout(self):
        self.user.user_permissions.add(Permission.objects.get(codename="change_crop"))

        response = self.client.patch(self.update_url, {"notes": "Updated notes"})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.crop.refresh_from_db()
        self.assertEqual(self.crop.layout, self.layout)
        self.assertEqual(self.crop.notes, "Updated notes")


class ObservationAPITests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="observation-api-user", password="testpass")
        self.other_user = User.objects.create_user(username="other-observation-user", password="testpass")
        self.client.force_authenticate(self.user)
        self.crop = CropFactory()
        self.state = StateFactory(trait__protocol__plantspecies=self.crop.variety.species)
        self.parameter = ParameterFactory()

    def grant(self, *codenames):
        self.user.user_permissions.add(*(Permission.objects.get(codename=codename) for codename in codenames))
        self.user = User.objects.get(pk=self.user.pk)
        self.client.force_authenticate(self.user)

    def jsonl_rows(self, response):
        content = b"".join(response.streaming_content).decode()
        return [json.loads(line) for line in content.splitlines()]

    def test_trait_creation_validates_species_and_assigns_authenticated_user(self):
        self.grant("add_traitobservation")
        recorded_at = timezone.now().replace(microsecond=0)
        response = self.client.post(
            reverse("restapi:trait-observations-list"),
            {
                "crop": self.crop.pk,
                "state": self.state.pk,
                "recorded_at": recorded_at.isoformat(),
                "created_by": self.other_user.pk,
            },
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        observation = TraitObservation.objects.get(pk=response.data["id"])
        self.assertEqual(observation.created_by, self.user)
        self.assertEqual(observation.recorded_at, recorded_at)

        incompatible_state = StateFactory()
        response = self.client.post(
            reverse("restapi:trait-observations-list"),
            {"crop": self.crop.pk, "state": incompatible_state.pk},
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("state", response.data)

    def test_parameter_creation_accepts_value_or_date_and_rejects_neither(self):
        self.grant("add_parameterobservation")
        url = reverse("restapi:parameter-observations-list")

        value_response = self.client.post(
            url,
            {"crop": self.crop.pk, "parameter": self.parameter.pk, "parameter_value": "4.250"},
        )
        date_response = self.client.post(
            url,
            {"crop": self.crop.pk, "parameter": self.parameter.pk, "parameter_date": "2026-05-20"},
        )
        empty_response = self.client.post(url, {"crop": self.crop.pk, "parameter": self.parameter.pk})

        self.assertEqual(value_response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(date_response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(empty_response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_archived_observations_are_readable_and_exportable_but_immutable(self):
        observation = TraitObservationFactory(crop=self.crop, state=self.state, created_by=self.user)
        self.crop.layout.archive()
        self.grant("view_traitobservation", "add_traitobservation", "delete_traitobservation")
        detail_url = reverse("restapi:trait-observations-detail", args=[observation.pk])

        retrieve_response = self.client.get(detail_url)
        export_response = self.client.get(reverse("restapi:trait-observations-export-jsonl"))
        create_response = self.client.post(
            reverse("restapi:trait-observations-list"),
            {"crop": self.crop.pk, "state": self.state.pk},
        )
        delete_response = self.client.delete(detail_url)

        exported_rows = self.jsonl_rows(export_response)
        self.assertEqual(retrieve_response.status_code, status.HTTP_200_OK)
        self.assertEqual(export_response.status_code, status.HTTP_200_OK)
        self.assertEqual([row["id"] for row in exported_rows], [observation.pk])
        self.assertEqual(create_response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(delete_response.status_code, status.HTTP_404_NOT_FOUND)

    def test_active_deletion_requires_model_permission(self):
        observation = ParameterObservationFactory(crop=self.crop, created_by=self.user)
        url = reverse("restapi:parameter-observations-detail", args=[observation.pk])

        denied_response = self.client.delete(url)
        self.grant("delete_parameterobservation")
        allowed_response = self.client.delete(url)

        self.assertEqual(denied_response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(allowed_response.status_code, status.HTTP_204_NO_CONTENT)

    def test_list_and_export_apply_relation_filters(self):
        self.grant("view_traitobservation", "view_parameterobservation")
        trait_observation = TraitObservationFactory(crop=self.crop, state=self.state, created_by=self.user)
        TraitObservationFactory(created_by=self.user)
        parameter_observation = ParameterObservationFactory(
            crop=self.crop,
            parameter=self.parameter,
            created_by=self.user,
        )
        ParameterObservationFactory(created_by=self.user)

        trait_response = self.client.get(
            reverse("restapi:trait-observations-list"),
            {"protocol": self.state.trait.protocol_id},
        )
        parameter_export = self.client.get(
            reverse("restapi:parameter-observations-export-jsonl"),
            {"parameter": self.parameter.pk},
        )
        exported_rows = self.jsonl_rows(parameter_export)

        self.assertEqual([row["id"] for row in trait_response.data["results"]], [trait_observation.pk])
        self.assertEqual([row["id"] for row in exported_rows], [parameter_observation.pk])


class ArchivedLayoutAPITests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="archived-layout-api-user", password="testpass")
        self.client.force_authenticate(self.user)
        self.layout = CropLayoutFactory(archived_at=timezone.now())
        self.crop = CropFactory(layout=self.layout, notes="Archived crop notes")

    def test_archived_layout_cannot_be_updated(self):
        self.user.user_permissions.add(Permission.objects.get(codename="change_croplayout"))

        response = self.client.patch(
            reverse("restapi:crop-layout-detail", args=[self.layout.pk]),
            {"name": "Updated archived layout"},
        )

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.layout.refresh_from_db()
        self.assertNotEqual(self.layout.name, "Updated archived layout")

    def test_archived_at_cannot_be_changed_through_layout_updates(self):
        self.user.user_permissions.add(Permission.objects.get(codename="change_croplayout"))
        visible_layout = CropLayoutFactory()

        response = self.client.patch(
            reverse("restapi:crop-layout-detail", args=[visible_layout.pk]),
            {"archived_at": timezone.now().isoformat()},
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        visible_layout.refresh_from_db()
        self.assertIsNone(visible_layout.archived_at)

    def test_archived_layout_can_be_deleted_when_deletable(self):
        self.user.user_permissions.add(Permission.objects.get(codename="delete_croplayout"))
        deletable_layout = CropLayoutFactory(archived_at=timezone.now())

        response = self.client.delete(reverse("restapi:crop-layout-detail", args=[deletable_layout.pk]))

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(type(deletable_layout).objects.filter(pk=deletable_layout.pk).exists())

    def test_protected_layout_deletion_returns_conflict(self):
        self.user.user_permissions.add(Permission.objects.get(codename="delete_croplayout"))

        response = self.client.delete(reverse("restapi:crop-layout-detail", args=[self.layout.pk]))

        self.assertEqual(response.status_code, status.HTTP_409_CONFLICT)
        self.assertEqual(response.data, {"detail": self.layout.cant_delete_msg})
        self.assertTrue(type(self.layout).objects.filter(pk=self.layout.pk).exists())
        self.assertTrue(Crop.objects.filter(pk=self.crop.pk).exists())

    def test_crop_cannot_be_created_in_archived_layout(self):
        self.user.user_permissions.add(Permission.objects.get(codename="add_crop"))
        variety = PlantVarietyFactory()

        response = self.client.post(
            reverse("restapi:crops-list"),
            {"layout": self.layout.pk, "variety": variety.pk},
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("layout", response.data)
        self.assertFalse(Crop.objects.filter(layout=self.layout, variety=variety).exists())

    def test_crop_in_archived_layout_cannot_be_updated_or_deleted(self):
        self.user.user_permissions.add(
            Permission.objects.get(codename="change_crop"),
            Permission.objects.get(codename="delete_crop"),
        )
        url = reverse("restapi:crops-detail", args=[self.crop.pk])

        update_response = self.client.patch(url, {"notes": "Changed notes"})
        delete_response = self.client.delete(url)

        self.assertEqual(update_response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(delete_response.status_code, status.HTTP_404_NOT_FOUND)
        self.crop.refresh_from_db()
        self.assertEqual(self.crop.notes, "Archived crop notes")

    def test_crop_import_rejects_archived_layout(self):
        self.user.user_permissions.add(Permission.objects.get(codename="add_crop"))
        variety = PlantVarietyFactory()
        csv_content = f"layout,variety,notes\n{self.layout.pk},{variety.pk},Imported crop\n".encode()

        for validate_only in (False, True):
            with self.subTest(validate_only=validate_only):
                uploaded_file = SimpleUploadedFile("crops.csv", csv_content, content_type="text/csv")
                response = self.client.post(
                    reverse("restapi:crops-excel-import"),
                    {"file": uploaded_file, "validate_only": validate_only},
                )

                self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
                self.assertFalse(Crop.objects.filter(layout=self.layout, variety=variety).exists())
