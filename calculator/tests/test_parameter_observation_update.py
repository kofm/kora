from datetime import date
from decimal import Decimal

from django.contrib.auth.models import Permission
from django.test import TestCase
from django.urls import reverse

from calculator.factories import ParameterObservationFactory, StepFactory
from calculator.models import ParameterObservation, ParameterTarget
from frontpage.factories import UserFactory
from parameters.factories import ParameterFactory


class ParameterObservationUpdateTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = UserFactory(username="parameter-editor")
        cls.user.user_permissions.add(
            Permission.objects.get(codename="change_parameterobservation"),
            Permission.objects.get(codename="delete_parameterobservation"),
        )
        cls.step = StepFactory()
        cls.parameter = ParameterFactory()
        cls.other_parameter = ParameterFactory()
        ParameterTarget.objects.create(step=cls.step, parameter=cls.parameter)

    def setUp(self):
        self.client.force_login(self.user)
        self.observation = ParameterObservationFactory(
            crop=self.step.crop,
            step=self.step,
            parameter=self.parameter,
            parameter_value=Decimal("1.000"),
            notes="Original notes",
            created_by=self.user,
        )

    def test_update_changes_editable_fields_without_changing_associations(self):
        recorded_at = self.observation.recorded_at
        response = self.client.post(
            reverse("calculator:parameter_observation_update", args=(self.observation.pk,)),
            {
                "parameter_value": "2.500",
                "parameter_date": "2025-04-03",
                "notes": "Updated notes",
                "parameter": self.other_parameter.pk,
                "crop": self.step.crop.pk,
                "step": "",
                "created_by": UserFactory().pk,
                "recorded_at": "2020-01-01T00:00:00Z",
            },
        )

        self.observation.refresh_from_db()
        self.assertEqual(self.observation.parameter_value, Decimal("2.500"))
        self.assertEqual(self.observation.parameter_date, date(2025, 4, 3))
        self.assertEqual(self.observation.notes, "Updated notes")
        self.assertEqual(self.observation.parameter, self.parameter)
        self.assertEqual(self.observation.crop, self.step.crop)
        self.assertEqual(self.observation.step, self.step)
        self.assertEqual(self.observation.created_by, self.user)
        self.assertEqual(self.observation.recorded_at, recorded_at)
        self.assertJSONEqual(
            response.headers["HX-Trigger"],
            {"closeModal": True, "observationParameterUpdated": True},
        )

    def test_update_rejects_clearing_value_and_date(self):
        response = self.client.post(
            reverse("calculator:parameter_observation_update", args=(self.observation.pk,)),
            {"parameter_value": "", "parameter_date": "", "notes": "Updated notes"},
        )

        self.assertEqual(response.status_code, 200)
        self.assertFormError(
            response.context["form"],
            None,
            "Constraint “at_least_one_of_value_or_date” is violated.",
        )
        self.observation.refresh_from_db()
        self.assertEqual(self.observation.parameter_value, Decimal("1.000"))
        self.assertIsNone(self.observation.parameter_date)
        self.assertEqual(self.observation.notes, "Original notes")

    def test_delete_removes_observation_and_emits_refresh_events(self):
        response = self.client.post(reverse("calculator:parameter_observation_delete", args=(self.observation.pk,)))

        self.assertFalse(ParameterObservation.objects.filter(pk=self.observation.pk).exists())
        self.assertJSONEqual(
            response.headers["HX-Trigger"],
            {"closeModal": True, "observationParameterUpdated": True},
        )
