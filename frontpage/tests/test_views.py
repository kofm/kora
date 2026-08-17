from django.test import RequestFactory, SimpleTestCase, TestCase
from django.urls import reverse

from frontpage.factories import AdminFactory
from frontpage.utils.shortcuts import get_safe_next_url


class ViewSmokeTests(TestCase):
    def setUp(self):
        self.user = AdminFactory(username="tester", password="pass")
        self.client.login(username="tester", password="pass")

    def test_admin_view(self):
        response = self.client.get(reverse("frontpage:admin"))
        self.assertEqual(response.status_code, 200)


class SafeNextUrlTests(SimpleTestCase):
    def setUp(self):
        self.request_factory = RequestFactory()

    def test_accepts_same_host_path(self):
        request = self.request_factory.get("/update", {"next": "/parameters/varietalparameters"})

        self.assertEqual(get_safe_next_url(request, "/fallback"), "/parameters/varietalparameters")

    def test_rejects_external_url(self):
        request = self.request_factory.get("/update", {"next": "https://example.com/redirect"})

        self.assertEqual(get_safe_next_url(request, "/fallback"), "/fallback")
