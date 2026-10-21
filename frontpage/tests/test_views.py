from django.contrib.auth.models import Permission
from django.test import RequestFactory, SimpleTestCase, TestCase
from django.urls import reverse

from frontpage.factories import AdminFactory
from frontpage.utils.shortcuts import get_safe_next_url


class AppearancePreferenceTests(TestCase):
    def test_anonymous_user_can_persist_auto(self):
        session = self.client.session
        session["appearance"] = "dark"
        session.save()

        response = self.client.post(reverse("frontpage:appearance_set"), {"appearance": "auto"})

        self.assertEqual(response.status_code, 200)
        self.assertEqual(self.client.session["appearance"], "auto")

    def test_invalid_submission_preserves_saved_preference(self):
        session = self.client.session
        session["appearance"] = "dark"
        session.save()

        for data in ({}, {"appearance": ""}, {"appearance": "unsupported"}):
            with self.subTest(data=data):
                response = self.client.post(reverse("frontpage:appearance_set"), data)
                self.assertEqual(response.status_code, 400)
                self.assertEqual(self.client.session["appearance"], "dark")


class ViewSmokeTests(TestCase):
    def setUp(self):
        self.user = AdminFactory(username="tester", password="pass")
        self.user.user_permissions.add(Permission.objects.get(codename="view_user"))
        self.client.login(username="tester", password="pass")

    def test_admin_view(self):
        response = self.client.get(reverse("frontpage:admin"))
        self.assertEqual(response.status_code, 200)

    def test_user_list_refresh_returns_only_the_users_region(self):
        response = self.client.get(
            reverse("frontpage:admin"), {"partial": "users", "sort": "username"}, HTTP_HX_REQUEST="true"
        )

        self.assertContains(response, 'id="users"', count=1)
        self.assertContains(response, self.user.username)
        self.assertNotContains(response, 'id="navbar-admin"')


class AccountAdministrationPermissionTests(TestCase):
    def test_staff_status_alone_does_not_allow_user_administration(self):
        staff_user = AdminFactory(username="staff-only", password="pass", is_superuser=False)
        self.client.force_login(staff_user)

        response = self.client.get(reverse("frontpage:admin"))

        self.assertEqual(response.status_code, 403)


class SafeNextUrlTests(SimpleTestCase):
    def setUp(self):
        self.request_factory = RequestFactory()

    def test_accepts_same_host_path(self):
        request = self.request_factory.get("/update", {"next": "/parameters/varietalparameters"})

        self.assertEqual(get_safe_next_url(request, "/fallback"), "/parameters/varietalparameters")

    def test_rejects_external_url(self):
        request = self.request_factory.get("/update", {"next": "https://example.com/redirect"})

        self.assertEqual(get_safe_next_url(request, "/fallback"), "/fallback")
