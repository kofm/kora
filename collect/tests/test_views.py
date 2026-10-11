from django.test import TestCase
from django.urls import reverse

from collect.factories import SampleFactory
from frontpage.factories import UserFactory


class SampleSearchViewTests(TestCase):
    def test_id_search_keeps_discarded_results_separate_and_counted(self):
        self.client.force_login(UserFactory(is_superuser=True, is_staff=True))
        discarded = SampleFactory(sample_id=123)
        discarded.discard()
        SampleFactory(sample_id=1234)

        response = self.client.get(reverse("collect:sample_list"), {"omni": "123"})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(list(response.context["table"].data), [])
        self.assertEqual(response.context["discarded_count"], 1)
        self.assertContains(response, f'{reverse("collect:discarded_sample_list")}?omni=123')

        response = self.client.get(reverse("collect:discarded_sample_list"), {"omni": "123"})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(list(response.context["table"].data), [discarded])
