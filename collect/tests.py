from django.test import TestCase

from collect.models import Germinability, SeedSample, Storage, StoragePosition
from collect.tables import SeedSampleTableMixin
from register.models import Entity, PlantSpecies, PlantVariety


class SeedSampleTestCase(TestCase):
    def setUp(self):
        wheat = PlantSpecies.objects.create(
            latin_name="Triticum aestivum", common_name="Wheat", plant_type="herbaceous"
        )
        nstrampelli = Entity.objects.create(name="Nazareno Strampelli", type="IN", country="IT")
        rieti = PlantVariety.objects.create(name="Rieti", species=wheat, breeder=nstrampelli)
        self.rieti_originario = PlantVariety.objects.create(name="Rieti originario", species=wheat)
        storage = Storage.objects.create(name="S101", order=0)
        storagepos1 = StoragePosition.objects.create(name="1", storage=storage)
        storagepos2 = StoragePosition.objects.create(name="2", storage=storage)
        self.record_rieti = SeedSample.objects.create(sample_id=1, position=storagepos1, variety=rieti)
        self.record_rieti_originario = SeedSample.objects.create(
            sample_id=2, position=storagepos2, variety=self.rieti_originario
        )
        Germinability.objects.create(
            seedsample=self.record_rieti,
            germinability=85,
        )
        self.mixin = SeedSampleTableMixin()

    def test_render_germinability(self):
        """Germinability is correctly rendered"""
        self.assertEqual(self.mixin.render_germinability(self.record_rieti), "85%")


from django.test import TestCase
from django.urls import reverse

from .models import Storage, StoragePosition


class StorageCreateViewTests(TestCase):
    def setUp(self):
        pass

    def test_view_url_accessible_by_name(self):
        response = self.client.get(reverse("collect:storage-create"))
        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        response = self.client.get(reverse("collect:storage-create"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "collect/storage_form.html")

    def test_post_with_valid_data_creates_storage(self):
        url = reverse("collect:storage-create")
        data = {
            "name": "Test Storage",  # Assuming your form has a 'name' field
            "positions": 5,  # And a 'positions' field to indicate the number of positions to create
        }
        response = self.client.post(url, data)
        self.assertEqual(Storage.objects.count(), 1)
        self.assertEqual(StoragePosition.objects.count(), 5)

        storage = Storage.objects.first()
        self.assertRedirects(response, reverse("collect:storage_detail", args=[storage.pk]))

    def test_post_with_invalid_data(self):
        url = reverse("collect:storage-create")
        data = {"positions": ""}  # Empty data or intentionally invalid data based on your form validations
        response = self.client.post(url, data)
        self.assertEqual(Storage.objects.count(), 0)
        self.assertFormError(response, "form", "name", "This field is required.")  # Example for a required field error

    def test_create_another_redirects_correctly(self):
        url = reverse("collect:storage-create")
        data = {
            "name": "Another Test Storage",
            "positions": 3,
            "btn-another": True,  # Simulate clicking the 'create another' button
        }
        response = self.client.post(url, data)
        self.assertRedirects(response, reverse("collect:storage-create"))
