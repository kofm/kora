from django.test import TestCase

from collect.factories import SampleFactory
from collect.filters import SampleFilter
from collect.models import Sample
from register.factories import PlantVarietyNameFactory


class SampleFilterTests(TestCase):
    def matches(self, query, **filters):
        return list(SampleFilter({"omni": query, **filters}, queryset=Sample.objects.all()).qs)

    def test_numeric_search_matches_exact_sample_id_not_primary_key_or_partial_id(self):
        target = SampleFactory(sample_id=123)
        SampleFactory(sample_id=1234)
        SampleFactory(pk=123, sample_id=456)

        self.assertEqual(self.matches("123"), [target])

    def test_numeric_search_preserves_text_matches_without_duplicate_samples(self):
        by_id = SampleFactory(sample_id=123)
        by_notes = SampleFactory(sample_id=456, notes="Stored in 123 bin")
        by_name = SampleFactory(sample_id=789)
        PlantVarietyNameFactory(variety=by_name.variety, name="Line 123")
        PlantVarietyNameFactory(variety=by_name.variety, name="Line 123 alternate")

        self.assertCountEqual(self.matches("123"), [by_id, by_notes, by_name])

    def test_species_filter_still_narrows_sample_id_matches(self):
        target = SampleFactory(sample_id=123)
        other = SampleFactory(sample_id=456)
        self.assertNotEqual(target.variety.species_id, other.variety.species_id)

        self.assertEqual(self.matches("123", variety__species=[other.variety.species_id]), [])

    def test_text_and_out_of_range_numeric_search_remain_usable(self):
        target = SampleFactory(sample_id=123, notes="Seed lot 999999999999999999999999")

        for query in ("Seed lot", "999999999999999999999999"):
            with self.subTest(query=query):
                self.assertEqual(self.matches(query), [target])
