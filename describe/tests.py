from django.test import TestCase

from .models import PlantVariety
from register.models import Entity

class PlantVarietyModelTests(TestCase):
    
    def test_has_breeder(self):
        """
        has_breeder() should return True if a Entity is associated with the variety as the breeder
        """
        entity = Entity(name = "A fake name")
        variety = PlantVariety(name = "A test variety", breeder = entity)
        self.assertIs(variety.has_breeder(), True)
