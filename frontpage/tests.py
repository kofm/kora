from django.test import TestCase
from django.urls import reverse

from frontpage.factories import AdminFactory


class ViewSmokeTests(TestCase):
    def setUp(self):
        self.user = AdminFactory(username="tester", password="pass")
        self.client.login(username="tester", password="pass")

    def test_admin_view(self):
        response = self.client.get(reverse("frontpage:admin"))
        self.assertEqual(response.status_code, 200)
