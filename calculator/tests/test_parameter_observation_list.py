from datetime import date, datetime
from decimal import Decimal

from django.contrib.auth.models import Permission
from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from calculator.factories import (
    CropFactory,
    CropLayoutFactory,
    FieldBookFactory,
    ParameterObservationFactory,
    StepFactory,
)
from calculator.models import ParameterTarget
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

    def test_location_and_fieldbook_or_layout_filters_use_or_matching(self):
        selected_location = self.crop.layout.location
        fieldbook_layout = CropLayoutFactory(name="Unrelated layout", location=selected_location)
        fieldbook_crop = CropFactory(layout=fieldbook_layout)
        matching_fieldbook = FieldBookFactory(name="Needle field book", layout=fieldbook_layout)
        matching_step = StepFactory(fieldbook=matching_fieldbook, crop=fieldbook_crop)
        ParameterTarget.objects.create(step=matching_step, parameter=self.parameter)
        fieldbook_match = ParameterObservationFactory(
            crop=fieldbook_crop,
            step=matching_step,
            parameter=self.parameter,
        )

        layout_match_layout = CropLayoutFactory(name="Needle archived layout", location=selected_location)
        layout_match_layout.archive()
        layout_match = ParameterObservationFactory(
            crop=CropFactory(layout=layout_match_layout),
            parameter=self.parameter,
        )
        ParameterObservationFactory(
            crop=CropFactory(layout=CropLayoutFactory(name="Unrelated selected layout", location=selected_location)),
            parameter=self.parameter,
        )
        ParameterObservationFactory(
            crop=CropFactory(layout=CropLayoutFactory(name="Needle other location")),
            parameter=self.parameter,
        )

        response = self.client.get(
            self.url,
            {"location": [selected_location.pk], "fieldbook_or_layout": "needle"},
        )

        self.assertCountEqual(response.context["table"].data, [fieldbook_match, layout_match])
