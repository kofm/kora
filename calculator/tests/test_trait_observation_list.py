from datetime import datetime

from django.contrib.auth.models import Permission
from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from calculator.factories import CropFactory, CropLayoutFactory, FieldBookFactory, StepFactory
from calculator.models import TraitObservation, TraitTarget
from describe.factories import ProtocolFactory, StateFactory, TraitFactory
from frontpage.factories import UserFactory
from register.factories import PlantSpeciesFactory, PlantVarietyFactory


class TraitObservationListTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = UserFactory(username="viewer", password="x")
        cls.user.user_permissions.add(Permission.objects.get(codename="view_traitobservation"))
        cls.url = reverse("calculator:trait_observation_list")

        cls.wheat = PlantSpeciesFactory(common_name="Wheat", latin_name="Triticum", plant_type="herbaceous")
        cls.rice = PlantSpeciesFactory(common_name="Rice", latin_name="Oryza", plant_type="herbaceous")
        cls.wheat_variety = PlantVarietyFactory(name="Wheat A", species=cls.wheat)
        cls.other_wheat_variety = PlantVarietyFactory(name="Wheat B", species=cls.wheat)
        cls.unselected_wheat_variety = PlantVarietyFactory(name="Wheat C", species=cls.wheat)
        cls.rice_variety = PlantVarietyFactory(name="Rice A", species=cls.rice)

        cls.wheat_protocol = ProtocolFactory(name="Wheat protocol", plantspecies=cls.wheat)
        cls.rice_protocol = ProtocolFactory(name="Rice protocol", plantspecies=cls.rice)
        cls.height = TraitFactory(numeric_id=1, description="Height", protocol=cls.wheat_protocol)
        cls.colour = TraitFactory(numeric_id=2, description="Colour", protocol=cls.wheat_protocol)
        cls.rice_height = TraitFactory(numeric_id=1, description="Rice height", protocol=cls.rice_protocol)
        cls.tall = StateFactory(numeric_id=1, description="Tall", trait=cls.height)
        cls.short = StateFactory(numeric_id=2, description="Short", trait=cls.height)
        cls.green = StateFactory(numeric_id=1, description="Green", trait=cls.colour)
        cls.rice_tall = StateFactory(numeric_id=1, description="Rice tall", trait=cls.rice_height)

        cls.layout = CropLayoutFactory(name="Current layout")
        cls.archived_layout = CropLayoutFactory(name="Archived layout")
        cls.archived_layout.archive()
        cls.matching_crop = CropFactory(layout=cls.archived_layout, variety=cls.wheat_variety, order=0)
        cls.other_matching_crop = CropFactory(layout=cls.layout, variety=cls.other_wheat_variety, order=0)
        cls.unselected_variety_crop = CropFactory(layout=cls.layout, variety=cls.unselected_wheat_variety, order=1)
        cls.rice_crop = CropFactory(layout=cls.layout, variety=cls.rice_variety, order=2)

        cls.matching = TraitObservation.objects.create(
            crop=cls.matching_crop,
            state=cls.tall,
            created_by=cls.user,
            recorded_at=timezone.make_aware(datetime(2025, 2, 15, 12)),
        )
        cls.other_matching = TraitObservation.objects.create(
            crop=cls.other_matching_crop,
            state=cls.tall,
            created_by=cls.user,
            recorded_at=timezone.make_aware(datetime(2025, 2, 15, 12)),
        )
        TraitObservation.objects.create(
            crop=cls.unselected_variety_crop,
            state=cls.tall,
            created_by=cls.user,
            recorded_at=timezone.make_aware(datetime(2025, 2, 15, 12)),
        )
        TraitObservation.objects.create(
            crop=cls.matching_crop,
            state=cls.short,
            created_by=cls.user,
            recorded_at=timezone.make_aware(datetime(2025, 2, 16, 12)),
        )
        TraitObservation.objects.create(
            crop=cls.matching_crop,
            state=cls.green,
            created_by=cls.user,
            recorded_at=timezone.make_aware(datetime(2025, 2, 15, 12)),
        )
        TraitObservation.objects.create(
            crop=cls.rice_crop,
            state=cls.rice_tall,
            created_by=cls.user,
            recorded_at=timezone.make_aware(datetime(2025, 2, 15, 12)),
        )
        TraitObservation.objects.create(
            crop=cls.matching_crop,
            state=cls.tall,
            created_by=cls.user,
            recorded_at=timezone.make_aware(datetime(2025, 3, 1, 12)),
        )

    def setUp(self):
        self.client.force_login(self.user)

    def test_combined_filters_include_selected_varieties_and_archived_layout_observation(self):
        response = self.client.get(
            self.url,
            {
                "species": self.wheat.pk,
                "variety": [self.wheat_variety.pk, self.other_wheat_variety.pk],
                "protocol": self.wheat_protocol.pk,
                "trait": self.height.pk,
                "recorded_at_start": "2025-02-15",
                "recorded_at_end": "2025-02-15",
            },
        )

        self.assertCountEqual(response.context["table"].data, [self.matching, self.other_matching])

    def test_location_and_fieldbook_or_layout_filters_use_or_matching(self):
        selected_location = self.layout.location
        fieldbook_layout = CropLayoutFactory(name="Unrelated layout", location=selected_location)
        fieldbook_crop = CropFactory(layout=fieldbook_layout, variety=self.wheat_variety)
        matching_fieldbook = FieldBookFactory(name="Needle field book", layout=fieldbook_layout)
        matching_step = StepFactory(fieldbook=matching_fieldbook, crop=fieldbook_crop)
        TraitTarget.objects.create(step=matching_step, trait=self.height)
        fieldbook_match = TraitObservation.objects.create(
            crop=fieldbook_crop,
            step=matching_step,
            state=self.tall,
            created_by=self.user,
        )

        layout_match_layout = CropLayoutFactory(name="Needle archived layout", location=selected_location)
        layout_match_layout.archive()
        layout_match = TraitObservation.objects.create(
            crop=CropFactory(layout=layout_match_layout, variety=self.wheat_variety),
            state=self.tall,
            created_by=self.user,
        )
        TraitObservation.objects.create(
            crop=CropFactory(layout=CropLayoutFactory(name="Unrelated selected layout", location=selected_location)),
            state=self.tall,
            created_by=self.user,
        )
        TraitObservation.objects.create(
            crop=CropFactory(layout=CropLayoutFactory(name="Needle other location")),
            state=self.tall,
            created_by=self.user,
        )

        response = self.client.get(
            self.url,
            {"location": [selected_location.pk], "fieldbook_or_layout": "needle"},
        )

        self.assertCountEqual(response.context["table"].data, [fieldbook_match, layout_match])
