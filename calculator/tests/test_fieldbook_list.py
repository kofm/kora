from django.contrib.auth.models import Permission
from django.test import TestCase
from django.urls import reverse

from calculator.factories import CropFactory, CropLayoutFactory, FieldBookFactory, StepFactory
from calculator.models import ParameterObservation, ParameterTarget, TraitObservation, TraitTarget
from describe.factories import ProtocolFactory, StateFactory, TraitFactory
from frontpage.factories import UserFactory
from parameters.factories import ParameterFactory
from register.factories import PlantSpeciesFactory, PlantVarietyFactory


class FieldBookListTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = UserFactory(username="fieldbook-viewer", password="x")
        cls.user.user_permissions.add(Permission.objects.get(codename="view_fieldbook"))
        cls.layout = CropLayoutFactory(name="Visible layout")
        cls.fieldbook = FieldBookFactory(layout=cls.layout, name="Visible fieldbook")

        species = PlantSpeciesFactory(common_name="Wheat", latin_name="Triticum aestivum")
        variety = PlantVarietyFactory(species=species)
        first_crop = CropFactory(layout=cls.layout, variety=variety)
        second_crop = CropFactory(layout=cls.layout, variety=variety)
        first_step = StepFactory(fieldbook=cls.fieldbook, crop=first_crop)
        second_step = StepFactory(fieldbook=cls.fieldbook, crop=second_crop)

        protocol = ProtocolFactory(plantspecies=species)
        first_trait = TraitFactory(protocol=protocol)
        second_trait = TraitFactory(protocol=protocol)
        first_state = StateFactory(trait=first_trait)
        second_state = StateFactory(trait=second_trait)
        parameter = ParameterFactory()

        TraitTarget.objects.create(step=first_step, trait=first_trait, required_count=2)
        TraitTarget.objects.create(step=second_step, trait=second_trait)
        ParameterTarget.objects.create(step=first_step, parameter=parameter)
        TraitObservation.objects.create(
            crop=first_crop,
            step=first_step,
            state=first_state,
            created_by=cls.user,
        )
        TraitObservation.objects.create(
            crop=second_crop,
            step=second_step,
            state=second_state,
            created_by=cls.user,
        )
        TraitObservation.objects.create(
            crop=second_crop,
            step=second_step,
            state=second_state,
            created_by=cls.user,
        )
        ParameterObservation.objects.create(
            crop=first_crop,
            step=first_step,
            parameter=parameter,
            parameter_value=1,
            created_by=cls.user,
        )
        ParameterObservation.objects.create(
            crop=first_crop,
            parameter=parameter,
            parameter_value=2,
            created_by=cls.user,
        )

        archived_layout = CropLayoutFactory(name="Archived layout")
        cls.archived_fieldbook = FieldBookFactory(layout=archived_layout, name="Archived fieldbook")
        archived_layout.archive()

    def setUp(self):
        self.client.force_login(self.user)

    def test_lists_visible_fieldbooks_with_target_progress(self):
        response = self.client.get(reverse("calculator:fieldbook_list"))

        self.assertContains(response, self.fieldbook.get_absolute_url())
        self.assertNotContains(response, self.archived_fieldbook.get_absolute_url())
        self.assertContains(response, "<td>4</td>", count=2, html=True)
        self.assertContains(response, "75.0%")
