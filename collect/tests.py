from django.test import TestCase
from collect.models import Germinability, SeedSample, Storage, StoragePosition
from collect.tables import SeedSampleTableMixin
from register.models import Entity, PlantSpecies, PlantVariety


class SeedSampleTestCase(TestCase):
    def setUp(self):
        wheat = PlantSpecies.objects.create(
            latin_name="Triticum aestivum", common_name="Wheat", plant_type="herbaceous"
        )
        nstrampelli = Entity.objects.create(
            name="Nazareno Strampelli", type="IN", country="IT"
        )
        rieti = PlantVariety.objects.create(
            name="Rieti", species=wheat, breeder=nstrampelli
        )
        self.rieti_originario = PlantVariety.objects.create(
            name="Rieti originario", species=wheat
        )
        storage = Storage.objects.create(name="S101", order=0)
        storagepos1 = StoragePosition.objects.create(name="1", storage=storage)
        storagepos2 = StoragePosition.objects.create(name="2", storage=storage)
        self.record_rieti = SeedSample.objects.create(
            sample_id=1, position=storagepos1, variety=rieti
        )
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

    def test_render_variety(self):
        """Variety field is correctly rendered.
          It should print the breeder's country flag when
          available. Otherwise return the variety.
          """
        self.assertEqual(
            self.mixin.render_variety(self.record_rieti_originario),
            self.rieti_originario,
        )
        self.assertEqual(
            self.mixin.render_variety(self.record_rieti),
            "Rieti <i class='flag-sprite flag-i flag-_t'></i>",
        )
