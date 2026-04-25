from django.test import TestCase

from describe.forms import DescriptionForm
from describe.models import Description, Protocol
from register.models import PlantSpecies, PlantVariety


class DescriptionFormTest(TestCase):
    def setUp(self):
        species = PlantSpecies.objects.create(common_name="Rice", latin_name="Oryza sativa", plant_type="herbaceous")
        self.protocol = Protocol.objects.create(name="TP16/3", plantspecies=species)
        self.variety = PlantVariety.objects.create(name="Carnaroli", species=species)
        Description.objects.create(name="Existing Name 1", variety=self.variety, protocol=self.protocol)
        Description.objects.create(name="Existing Name 2", variety=self.variety, protocol=self.protocol)

    def test_form_validation_with_predefined_choice(self):
        """Test the form with a predefined choice for 'name'."""
        form_data = {"name": "Existing Name 1", "variety": self.variety.id, "protocol": self.protocol.id}
        form = DescriptionForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_form_validation_with_new_choice(self):
        """Test the form with a new 'name' value."""
        form_data = {"name": "New Name", "variety": self.variety.id, "protocol": self.protocol.id}
        form = DescriptionForm(data=form_data)
        self.assertTrue(form.is_valid())
