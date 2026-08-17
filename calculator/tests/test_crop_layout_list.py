from django.contrib.auth.models import Permission
from django.test import TestCase
from django.urls import reverse

from calculator.factories import CropLayoutFactory
from frontpage.factories import UserFactory
from spaces.factories import LocationFactory


class CropLayoutListTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = UserFactory(username="viewer", password="x")
        cls.permission = Permission.objects.get(codename="view_croplayout")
        cls.user.user_permissions.add(cls.permission)
        cls.url = reverse("calculator:croplayout_list")
        cls.location = LocationFactory(name="Main site")
        cls.visible_layout = CropLayoutFactory(location=cls.location, name="Alpha layout")
        cls.archived_layout = CropLayoutFactory(location=cls.location, name="Beta layout")
        cls.archived_layout.archive()

    def setUp(self):
        self.client.force_login(self.user)

    def test_status_filters_return_correct_layouts(self):
        for status, included_layouts, excluded_layouts in (
            (None, (self.visible_layout,), (self.archived_layout,)),
            ("visible", (self.visible_layout,), (self.archived_layout,)),
            ("archived", (self.archived_layout,), (self.visible_layout,)),
            ("all", (self.visible_layout, self.archived_layout), ()),
        ):
            with self.subTest(status=status):
                response = self.client.get(self.url, {"status": status} if status else {})

                for layout in included_layouts:
                    self.assertContains(response, layout.get_absolute_url())
                for layout in excluded_layouts:
                    self.assertNotContains(response, layout.get_absolute_url())

    def test_list_requires_view_permission(self):
        self.user.user_permissions.remove(self.permission)

        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 403)
