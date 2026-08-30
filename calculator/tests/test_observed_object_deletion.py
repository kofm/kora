from django.test import TestCase
from django.urls import reverse

from calculator.factories import CropFactory, ParameterObservationFactory
from calculator.models import TraitObservation
from describe.factories import ProtocolFactory, StateFactory, TraitFactory
from frontpage.factories import UserFactory


class ObservedObjectDeletionTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = UserFactory(is_superuser=True)
        cls.trait_crop = CropFactory()
        cls.protocol = ProtocolFactory(plantspecies=cls.trait_crop.variety.species)
        cls.trait = TraitFactory(protocol=cls.protocol)
        cls.state = StateFactory(trait=cls.trait)
        TraitObservation.objects.create(crop=cls.trait_crop, state=cls.state, created_by=cls.user)

        cls.parameter_crop = CropFactory()
        cls.parameter_observation = ParameterObservationFactory(crop=cls.parameter_crop, created_by=cls.user)
        cls.parameter = cls.parameter_observation.parameter

    def setUp(self):
        self.client.force_login(self.user)

    def test_observed_objects_are_not_deletable_through_established_endpoints(self):
        deletion_cases = (
            (self.state, "describe:state_delete", self.state.is_deletable),
            (self.trait, "describe:trait_delete", self.trait.is_deletable),
            (self.protocol, "describe:protocol_delete", self.protocol.is_deletable),
            (self.trait_crop, "calculator:crop_delete", self.trait_crop.is_deletable),
            (self.parameter, "parameters:parameter_delete", self.parameter.is_deletable),
            (self.parameter_crop, "calculator:crop_delete", self.parameter_crop.is_deletable),
        )

        for instance, view_name, is_deletable in deletion_cases:
            with self.subTest(model=instance._meta.label):
                self.assertFalse(is_deletable() if callable(is_deletable) else is_deletable)

                response = self.client.post(reverse(view_name, args=(instance.pk,)))

                self.assertEqual(response.status_code, 400)
                self.assertTrue(type(instance).objects.filter(pk=instance.pk).exists())
