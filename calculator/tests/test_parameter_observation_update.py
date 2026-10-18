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
            value_decimal=Decimal("1.000"),
            notes="Original notes",
            created_by=self.user,
        )

    def test_observation_headings_use_names_and_keep_units_on_numeric_inputs(self):
        self.user.user_permissions.add(
            Permission.objects.get(codename="add_parameterobservation"),
            Permission.objects.get(codename="view_step"),
        )
        self.parameter.name = "Stem length"
        self.parameter.measure_unit = "cm"
        self.parameter.save()
        target = ParameterTarget.objects.get(step=self.step, parameter=self.parameter)
        target.required_count = 2
        target.save()

        for view, pk, heading in (
            ("parameter_observation_update", self.observation.pk, '<h2 class="fs-5">Stem length</h2>'),
            ("parameter_target_observation_create", target.pk, '<h2 class="fs-5">Stem length</h2>'),
            (
                "step_detail",
                self.step.pk,
                '<span class="col-form-label fs-5 fw-semibold">Stem length</span>',
            ),
        ):
            with self.subTest(view=view):
                response = self.client.get(reverse(f"calculator:{view}", args=(pk,)))
                self.assertContains(response, heading, html=True)
                self.assertContains(response, 'class="input-group-text"')
                self.assertContains(response, ">cm</span>")

    def test_update_changes_editable_fields_without_changing_associations(self):
        recorded_at = self.observation.recorded_at
        response = self.client.post(
            reverse("calculator:parameter_observation_update", args=(self.observation.pk,)),
            {
                "value_decimal": "2.500",
                "notes": "Updated notes",
                "parameter": self.other_parameter.pk,
                "crop": self.step.crop.pk,
                "step": "",
                "created_by": UserFactory().pk,
                "recorded_at": "2020-01-01T00:00:00Z",
            },
        )

        self.observation.refresh_from_db()
        self.assertEqual(self.observation.value_decimal, Decimal("2.500"))
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

    def test_update_rejects_clearing_value(self):
        response = self.client.post(
            reverse("calculator:parameter_observation_update", args=(self.observation.pk,)),
            {"value_decimal": "", "notes": "Updated notes"},
        )

        self.assertEqual(response.status_code, 200)
        self.assertFormError(
            response.context["form"],
            "value_decimal",
            "This field is required.",
        )
        self.observation.refresh_from_db()
        self.assertEqual(self.observation.value_decimal, Decimal("1.000"))
        self.assertEqual(self.observation.notes, "Original notes")

    def test_delete_removes_observation_and_emits_refresh_events(self):
        response = self.client.post(reverse("calculator:parameter_observation_delete", args=(self.observation.pk,)))

        self.assertFalse(ParameterObservation.objects.filter(pk=self.observation.pk).exists())
        self.assertJSONEqual(
            response.headers["HX-Trigger"],
            {"closeModal": True, "observationParameterUpdated": True},
        )
