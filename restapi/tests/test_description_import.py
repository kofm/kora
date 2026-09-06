from django.contrib.auth.models import Permission, User
from django.core.files.uploadedfile import SimpleUploadedFile
from django.urls import reverse
from rest_framework.test import APIClient, APITestCase

from describe.factories import (
    DescriptionFactory,
    DescriptionLabelFactory,
    ProtocolFactory,
    StateFactory,
    TraitFactory,
)
from describe.models import Description, Expression
from register.factories import PlantSpeciesFactory, PlantVarietyFactory


class DescriptionImportTest(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username="testuser", password="testpass")
        self.user.user_permissions.add(
            *[
                Permission.objects.get(codename=codename)
                for codename in ("add_description", "add_expression")
            ]
        )
        self.client.login(username="testuser", password="testpass")

        self.species = PlantSpeciesFactory()
        self.variety = PlantVarietyFactory(name="antano", species=self.species)
        self.protocol = ProtocolFactory(plantspecies=self.species)
        self.label = DescriptionLabelFactory(name="Official")
        self.trait_1 = TraitFactory(protocol=self.protocol, numeric_id=1)
        self.trait_2 = TraitFactory(protocol=self.protocol, numeric_id=2)
        self.state_1_1 = StateFactory(trait=self.trait_1, numeric_id=1)
        self.state_1_2 = StateFactory(trait=self.trait_1, numeric_id=2)
        self.state_2_1 = StateFactory(trait=self.trait_2, numeric_id=1)

    def post_csv(self, csv_content, validate_only=False, protocol_id=None):
        uploaded_file = SimpleUploadedFile(
            "descriptions.csv",
            csv_content.encode(),
            content_type="text/csv",
        )
        data = {"file": uploaded_file, "validate_only": validate_only}
        if protocol_id is not None:
            data["protocol_id"] = protocol_id
        return self.client.post(reverse("restapi:descriptions-excel-import"), data, format="multipart")

    def test_import_creates_descriptions_and_expressions(self):
        csv_content = (
            "variety_name,label_name,notes,1,2\n"
            "antano,Official,Early maturing,1,1\n"
            "antano,,No label,2,\n"
        )

        response = self.post_csv(csv_content, protocol_id=self.protocol.pk)

        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json(), {"imported_rows": 2})

        descriptions = list(Description.objects.order_by("pk"))
        self.assertEqual(len(descriptions), 2)

        first = descriptions[0]
        self.assertEqual(first.variety, self.variety)
        self.assertEqual(first.protocol, self.protocol)
        self.assertEqual(first.label, self.label)
        self.assertEqual(first.notes, "Early maturing")
        self.assertSetEqual(
            set(first.expressions.values_list("state_id", flat=True)),
            {self.state_1_1.pk, self.state_2_1.pk},
        )

        second = descriptions[1]
        self.assertEqual(second.variety, self.variety)
        self.assertIsNone(second.label)
        self.assertEqual(second.notes, "No label")
        self.assertSetEqual(
            set(second.expressions.values_list("state_id", flat=True)),
            {self.state_1_2.pk},
        )

        self.assertTrue(all(expression.note == "" for expression in Expression.objects.all()))

    def test_existing_description_row_is_skipped(self):
        DescriptionFactory(variety=self.variety, protocol=self.protocol, label=self.label, notes="existing")
        csv_content = "variety_name,label_name,notes,1\nantano,Official,updated,1\n"

        response = self.post_csv(csv_content, protocol_id=self.protocol.pk)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"imported_rows": 0})
        self.assertEqual(Description.objects.count(), 1)
        self.assertEqual(Description.objects.get().notes, "existing")
        self.assertEqual(Expression.objects.count(), 0)

    def test_duplicate_rows_in_file_fail_whole_import(self):
        csv_content = (
            "variety_name,label_name,1\n"
            "antano,Official,1\n"
            "antano,Official,2\n"
        )

        response = self.post_csv(csv_content, protocol_id=self.protocol.pk)

        self.assertEqual(response.status_code, 400)
        self.assertEqual({row["row"] for row in response.data}, {2, 3})
        for row in response.data:
            self.assertIn("non_field_errors", row["error"])
        self.assertFalse(Description.objects.exists())
        self.assertFalse(Expression.objects.exists())

    def test_validate_only_imports_nothing(self):
        csv_content = "variety_name,label_name,notes,1\nantano,Official,Inspect me,1\n"

        response = self.post_csv(csv_content, validate_only=True, protocol_id=self.protocol.pk)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"imported_rows": 0})
        self.assertFalse(Description.objects.exists())
        self.assertFalse(Expression.objects.exists())

    def test_unknown_variety_name_fails(self):
        csv_content = "variety_name,label_name,1\nunknown,Official,1\n"

        response = self.post_csv(csv_content, protocol_id=self.protocol.pk)

        self.assertEqual(response.status_code, 400)
        self.assertIn("variety", response.data[0]["error"])
        self.assertFalse(Description.objects.exists())

    def test_ambiguous_variety_name_fails(self):
        PlantVarietyFactory(name="antano", species=self.species)
        csv_content = "variety_name,label_name,1\nantano,Official,1\n"

        response = self.post_csv(csv_content, protocol_id=self.protocol.pk)

        self.assertEqual(response.status_code, 400)
        self.assertIn("variety", response.data[0]["error"])
        self.assertFalse(Description.objects.exists())

    def test_unknown_label_fails(self):
        csv_content = "variety_name,label_name,1\nantano,MissingLabel,1\n"

        response = self.post_csv(csv_content, protocol_id=self.protocol.pk)

        self.assertEqual(response.status_code, 400)
        self.assertIn("label", response.data[0]["error"])
        self.assertFalse(Description.objects.exists())

    def test_invalid_trait_id_fails(self):
        csv_content = "variety_name,label_name,99\nantano,Official,1\n"

        response = self.post_csv(csv_content, protocol_id=self.protocol.pk)

        self.assertEqual(response.status_code, 400)
        self.assertIn("99", str(response.data[0]["error"]))
        self.assertFalse(Description.objects.exists())

    def test_invalid_state_id_fails(self):
        csv_content = "variety_name,label_name,1\nantano,Official,99\n"

        response = self.post_csv(csv_content, protocol_id=self.protocol.pk)

        self.assertEqual(response.status_code, 400)
        self.assertIn("99", str(response.data[0]["error"]))
        self.assertFalse(Description.objects.exists())

    def test_non_numeric_trait_cell_fails(self):
        csv_content = "variety_name,label_name,1\nantano,Official,abc\n"

        response = self.post_csv(csv_content, protocol_id=self.protocol.pk)

        self.assertEqual(response.status_code, 400)
        self.assertIn("not numeric", str(response.data[0]["error"]))
        self.assertFalse(Description.objects.exists())

    def test_missing_protocol_id_fails(self):
        csv_content = "variety_name,label_name,1\nantano,Official,1\n"
        uploaded_file = SimpleUploadedFile(
            "descriptions.csv",
            csv_content.encode(),
            content_type="text/csv",
        )

        response = self.client.post(
            reverse("restapi:descriptions-excel-import"),
            {"file": uploaded_file},
            format="multipart",
        )

        self.assertEqual(response.status_code, 400)
        self.assertIn("protocol_id", response.data)
        self.assertFalse(Description.objects.exists())
