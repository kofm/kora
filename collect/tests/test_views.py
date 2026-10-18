from django.test import TestCase
from django.urls import reverse

from collect.factories import SampleFactory, SampleWeightFactory
from frontpage.factories import UserFactory


class SampleSearchViewTests(TestCase):
    def test_id_search_keeps_discarded_results_separate_and_counted(self):
        self.client.force_login(UserFactory(is_superuser=True, is_staff=True))
        discarded = SampleFactory(sample_id=123)
        discarded.discard()
        SampleFactory(sample_id=1234)

        for headers in ({}, {"HTTP_HX_REQUEST": "true"}):
            with self.subTest(htmx=bool(headers)):
                response = self.client.get(reverse("collect:sample_list"), {"omni": "123"}, **headers)
                self.assertEqual(response.status_code, 200)
                self.assertEqual(list(response.context["table"].data), [])
                self.assertEqual(response.context["discarded_count"], 1)
                self.assertContains(response, f'{reverse("collect:discarded_sample_list")}?omni=123')

                response = self.client.get(reverse("collect:discarded_sample_list"), {"omni": "123"}, **headers)
                self.assertEqual(response.status_code, 200)
                self.assertEqual(list(response.context["table"].data), [discarded])
                self.assertContains(response, f'{reverse("collect:discarded_sample_bulk_delete")}?omni=123')


class SampleDetailRefreshTests(TestCase):
    def test_log_refresh_also_updates_weight_and_germinability_cards(self):
        self.client.force_login(UserFactory(is_superuser=True))
        sample = SampleFactory()
        SampleWeightFactory(sample=sample, weight=20)

        response = self.client.get(reverse("collect:sample_detail", args=[sample.pk]), HTTP_HX_REQUEST="true")

        self.assertContains(response, 'id="log"', count=1)
        self.assertContains(response, 'id="weightCard" hx-swap-oob="true"', count=1)
        self.assertContains(response, 'id="germinabilityCard" hx-swap-oob="true"', count=1)
        self.assertContains(response, sample.get_weight_display())
        self.assertNotContains(response, "Related Samples")
