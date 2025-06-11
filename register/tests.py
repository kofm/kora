from django.contrib.auth.models import Permission, User
from django.test import TestCase
from django.urls import reverse

from register.factories import PlantSpeciesFactory
from register.models import PlantVariety


class PlantVarietyCreateViewTests(TestCase):
    def setUp(self):
        self.species = PlantSpeciesFactory()
        self.user = User.objects.create_user(username="basicuser", password="password")
        self.perm_user = User.objects.create_user(username="permuser", password="password")
        permission = Permission.objects.get(codename="add_plantvariety")
        self.perm_user.user_permissions.add(permission)

        self.create_url = reverse("register:variety_create")

    def test_redirects_if_not_logged_in(self):
        response = self.client.get(self.create_url)
        self.assertRedirects(response, f"/accounts/login/?next={self.create_url}")

    def test_forbidden_if_no_permission(self):
        self.client.login(username="basicuser", password="password")
        response = self.client.get(self.create_url)
        self.assertEqual(response.status_code, 403)

    def test_get_with_permission(self):
        self.client.login(username="permuser", password="password")
        response = self.client.get(self.create_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "frontpage/_create_form.html")
        self.assertIn("model_name", response.context)

    def test_post_creates_plantvariety(self):
        self.client.login(username="permuser", password="password")
        response = self.client.post(
            self.create_url,
            {"name": "Cherry Tomato", "species": self.species.pk},
        )
        self.assertEqual(response.status_code, 302)
        self.assertTrue(PlantVariety.objects.filter(name="Cherry Tomato").exists())
