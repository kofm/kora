from unittest.mock import patch

from django.test import SimpleTestCase, override_settings
from django.urls import reverse


@override_settings(
    MIDDLEWARE=[
        "django.contrib.sessions.middleware.SessionMiddleware",
        "django.contrib.auth.middleware.AuthenticationMiddleware",
        "django.contrib.auth.middleware.LoginRequiredMiddleware",
    ]
)
class ReadinessTests(SimpleTestCase):
    def test_readiness_is_available_without_authentication_when_database_is_usable(self):
        with patch("persefone.views.connection.ensure_connection") as ensure_connection:
            response = self.client.get(reverse("readiness"))

        ensure_connection.assert_called_once_with()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content, b"ready\n")

    def test_readiness_fails_when_database_check_raises_error(self):
        with patch("persefone.views.connection.ensure_connection", side_effect=RuntimeError("database down")):
            response = self.client.get(reverse("readiness"))

        self.assertEqual(response.status_code, 503)
        self.assertEqual(response.content, b"database unavailable\n")
