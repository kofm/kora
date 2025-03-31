from django.test import TestCase

from describe.forms import DescriptionForm
from describe.models import Description, Protocol
from register.models import Entity, PlantSpecies, PlantVariety


class PlantVarietyModelTests(TestCase):
    def test_has_breeder(self):
        """
        has_breeder() should return True if a Entity is associated with the variety as the breeder
        """
        entity = Entity(name="A fake name")
        variety = PlantVariety(name="A test variety", breeder=entity)
        self.assertIs(variety.has_breeder(), True)


class DescriptionFormTest(TestCase):
    def setUp(self):
        species = PlantSpecies.objects.create(common_name="Rice", latin_name="Oryza sativa", plant_type="herbaceous")
        self.protocol = Protocol.objects.create(name="TP16/3", plantspecies=species)
        self.variety = PlantVariety.objects.create(name="Carnaroli", species=species)
        Description.objects.create(name="Existing Name 1", variety=self.variety, protocol=self.protocol)
        Description.objects.create(name="Existing Name 2", variety=self.variety, protocol=self.protocol)

    # def test_form_initialization(self):
    #     """Test that the form initializes with the correct choices."""
    #     form = DescriptionForm()
    #     expected_choices = Description.names()
    #     actual_choices = form.fields["name"].widget.choices
    #     self.assertEqual(list(actual_choices), expected_choices)

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
