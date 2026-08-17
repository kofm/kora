from django.contrib.auth.models import Permission
from django.test import TestCase
from django.urls import reverse

from calculator.factories import CropFactory
from calculator.models import TraitObservation
from describe.factories import ProtocolFactory, StateFactory, TraitFactory
from frontpage.factories import UserFactory
from register.factories import PlantSpeciesFactory


class TraitObservationCreateTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = UserFactory(username="observer")
        cls.user.user_permissions.add(Permission.objects.get(codename="add_traitobservation"))
        cls.crop = CropFactory()
        cls.protocol = ProtocolFactory(plantspecies=cls.crop.variety.species)
        cls.trait = TraitFactory(protocol=cls.protocol)
        cls.state = StateFactory(trait=cls.trait)
        cls.url = reverse("calculator:observation_expression_create", args=(cls.crop.pk,))

    def setUp(self):
        self.client.force_login(self.user)

    def test_creates_observation_for_valid_dependent_selection(self):
        response = self.client.post(
            self.url,
            {
                "protocol": self.protocol.pk,
                "trait": self.trait.pk,
                "state": self.state.pk,
                "notes": "Observed in the field",
            },
        )

        observation = TraitObservation.objects.get()
        self.assertEqual(observation.crop, self.crop)
        self.assertEqual(observation.created_by, self.user)
        self.assertEqual(observation.state, self.state)
        self.assertJSONEqual(response.headers["HX-Trigger"], {"closeModal": True, "traitObservationUpdated": True})

    def test_rejects_invalid_dependent_selections(self):
        other_protocol = ProtocolFactory(plantspecies=PlantSpeciesFactory())
        other_trait = TraitFactory(protocol=other_protocol)
        invalid_selections = (
            {
                "protocol": other_protocol.pk,
                "trait": other_trait.pk,
                "state": StateFactory(trait=other_trait).pk,
            },
            {
                "protocol": self.protocol.pk,
                "trait": self.trait.pk,
                "state": StateFactory(trait=TraitFactory(protocol=self.protocol)).pk,
            },
        )

        for selection in invalid_selections:
            with self.subTest(selection=selection):
                response = self.client.post(self.url, {**selection, "notes": ""})

                self.assertEqual(response.status_code, 200)
                self.assertFalse(TraitObservation.objects.exists())
