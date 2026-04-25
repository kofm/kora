from django.test import TestCase

from register.models import Entity, PlantVariety


class PlantVarietyModelTests(TestCase):
    def test_has_breeder(self):
        """
        has_breeder() should return True if a Entity is associated with the variety as the breeder
        """
        entity = Entity(name="A fake name")
        variety = PlantVariety(name="A test variety", breeder=entity)
        self.assertIs(variety.has_breeder(), True)
