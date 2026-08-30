from datetime import timedelta
from decimal import Decimal

from django.contrib.auth.models import Permission
from django.test import TestCase
from django.urls import reverse
from django.utils.timezone import now

from calculator.factories import ParameterObservationFactory, StepFactory
from calculator.layouts import FieldBookGrid
from calculator.models import ParameterObservation, ParameterTarget
from frontpage.factories import UserFactory
from parameters.factories import ParameterFactory


class FieldBookMapObservationTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = UserFactory(username="fieldbook-recorder")
        cls.user.user_permissions.add(
            Permission.objects.get(codename="view_fieldbook"),
            Permission.objects.get(codename="add_parameterobservation"),
            Permission.objects.get(codename="change_parameterobservation"),
        )
        cls.step = StepFactory()
        cls.parameter = ParameterFactory()
        cls.target = ParameterTarget.objects.create(step=cls.step, parameter=cls.parameter)
        cls.step_without_target = StepFactory(
            fieldbook=cls.step.fieldbook,
            crop__layout=cls.step.fieldbook.layout,
        )

    def grid_elements(self, field="value"):
        grid = FieldBookGrid(
            self.step.fieldbook.layout.crops.order_by("order"),
            fieldbook=self.step.fieldbook,
            display={"model": "parameter", "id": self.parameter.pk, "field": field},
            can_add_parameter_observation=True,
            can_change_parameter_observation=True,
        )
        return {element["object"].pk: element for element in grid.get_elements()}

    def test_only_plots_with_the_displayed_target_offer_observation_creation(self):
        elements = self.grid_elements()

        self.assertEqual(
            elements[self.step.crop_id]["body"]["display_mutation_url"],
            reverse("calculator:parameter_target_observation_create", args=(self.target.pk,)),
        )
        self.assertEqual(elements[self.step_without_target.crop_id]["body"]["display_mutation_url"], "")

    def test_blank_display_field_updates_the_latest_existing_observation(self):
        older_observation = ParameterObservationFactory(
            crop=self.step.crop,
            step=self.step,
            parameter=self.parameter,
            parameter_value=Decimal("4.000"),
            created_by=self.user,
            recorded_at=now() - timedelta(days=1),
        )
        latest_observation = ParameterObservationFactory(
            crop=self.step.crop,
            step=self.step,
            parameter=self.parameter,
            parameter_value=Decimal("0.000"),
            created_by=self.user,
            recorded_at=now(),
        )

        value_body = self.grid_elements()[self.step.crop_id]["body"]
        date_body = self.grid_elements(field="date")[self.step.crop_id]["body"]

        self.assertEqual(value_body["display_value"], Decimal("0.000"))
        self.assertEqual(
            value_body["display_mutation_url"],
            reverse("calculator:parameter_observation_update", args=(latest_observation.pk,)),
        )
        self.assertIsNone(date_body["display_value"])
        self.assertEqual(
            date_body["display_mutation_url"],
            reverse("calculator:parameter_observation_update", args=(latest_observation.pk,)),
        )
        self.assertNotIn(str(older_observation.pk), date_body["display_mutation_url"])

    def test_map_renders_zero_as_an_observed_value(self):
        self.client.force_login(self.user)
        ParameterObservationFactory(
            crop=self.step.crop,
            step=self.step,
            parameter=self.parameter,
            parameter_value=Decimal("0.000"),
            created_by=self.user,
        )
        self.step.fieldbook.set_display_config("parameter", self.parameter.pk)
        self.step.fieldbook.save()

        response = self.client.get(reverse("calculator:fieldbook_detail", args=(self.step.fieldbook.pk,)))

        self.assertContains(response, "0.000")

    def test_parameter_target_modal_rejects_a_forged_parameter(self):
        self.client.force_login(self.user)
        other_parameter = ParameterFactory()

        response = self.client.post(
            reverse("calculator:parameter_target_observation_create", args=(self.target.pk,)),
            {
                "parameter": other_parameter.pk,
                "parameter_value": "2.500",
                "parameter_date": "",
                "notes": "",
            },
        )

        self.assertEqual(response.status_code, 400)
        self.assertFalse(ParameterObservation.objects.filter(step=self.step).exists())
