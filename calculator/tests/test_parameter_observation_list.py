from datetime import date, datetime
from decimal import Decimal

from django.contrib.auth.models import Permission
from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from calculator.factories import CropFactory, ParameterObservationFactory
from frontpage.factories import UserFactory
from parameters.factories import ParameterFactory


class ParameterObservationListTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = UserFactory(username="parameter-viewer")
        cls.user.user_permissions.add(Permission.objects.get(codename="view_parameterobservation"))
        cls.url = reverse("calculator:parameter_observation_list")
        cls.parameter = ParameterFactory(code="STEM_LENGTH", name="Stem length")
        cls.other_parameter = ParameterFactory(code="LEAF_LENGTH", name="Leaf length")
        cls.crop = CropFactory()

    def setUp(self):
        self.client.force_login(self.user)

    def test_observation_lists_require_model_view_permission(self):
        unauthorized_user = UserFactory(username="observation-unauthorized")
        self.client.force_login(unauthorized_user)

        for url in (self.url, reverse("calculator:trait_observation_list")):
            with self.subTest(url=url):
                self.assertEqual(self.client.get(url).status_code, 403)

    def test_parameter_scoped_numeric_bounds_are_inclusive(self):
        lower_boundary = ParameterObservationFactory(
            crop=self.crop,
            parameter=self.parameter,
            parameter_value=Decimal("50"),
        )
        upper_boundary = ParameterObservationFactory(
            crop=self.crop,
            parameter=self.parameter,
            parameter_value=Decimal("60"),
        )
        ParameterObservationFactory(crop=self.crop, parameter=self.parameter, parameter_value=Decimal("49.999"))
        ParameterObservationFactory(crop=self.crop, parameter=self.parameter, parameter_value=Decimal("60.001"))
        ParameterObservationFactory(crop=self.crop, parameter=self.other_parameter, parameter_value=Decimal("55"))

        response = self.client.get(
            self.url,
            {"parameter": self.parameter.pk, "value_min": "50", "value_max": "60"},
        )

        self.assertCountEqual(response.context["table"].data, [lower_boundary, upper_boundary])

        response = self.client.get(self.url, {"value_min": "50", "value_max": "60"})

        self.assertEqual(len(response.context["table"].data), 3)

    def test_parameter_and_recorded_date_ranges_filter_independently(self):
        matching = ParameterObservationFactory(
            crop=self.crop,
            parameter=self.parameter,
            parameter_value=None,
            parameter_date=date(2025, 2, 15),
            recorded_at=timezone.make_aware(datetime(2025, 3, 10, 12)),
        )
        ParameterObservationFactory(
            crop=self.crop,
            parameter=self.parameter,
            parameter_value=None,
            parameter_date=date(2025, 2, 14),
            recorded_at=timezone.make_aware(datetime(2025, 3, 10, 12)),
        )
        ParameterObservationFactory(
            crop=self.crop,
            parameter=self.parameter,
            parameter_value=None,
            parameter_date=date(2025, 2, 15),
            recorded_at=timezone.make_aware(datetime(2025, 3, 11, 12)),
        )

        response = self.client.get(
            self.url,
            {
                "parameter_date_start": "2025-02-15",
                "parameter_date_end": "2025-02-15",
                "recorded_at_start": "2025-03-10",
                "recorded_at_end": "2025-03-10",
            },
        )

        self.assertCountEqual(response.context["table"].data, [matching])
