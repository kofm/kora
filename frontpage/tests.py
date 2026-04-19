from django.apps import apps
from django.template import TemplateSyntaxError
from django.test import SimpleTestCase, TestCase
from django.urls import reverse

from frontpage.factories import AdminFactory
from frontpage.templatetags.components import list_page_header
from frontpage.utils.assets import _ensure_assets


class ViewSmokeTests(TestCase):
    def setUp(self):
        self.user = AdminFactory(username="tester", password="pass")
        self.client.login(username="tester", password="pass")

    def test_admin_view(self):
        response = self.client.get(reverse("frontpage:admin"))
        self.assertEqual(response.status_code, 200)


class ListPageHeaderTests(TestCase):
    def setUp(self):
        self.user = AdminFactory(username="tester", password="pass")
        self.client.login(username="tester", password="pass")

    def test_list_page_header_uses_model_verbose_name_plural_as_default_title(self):
        response = self.client.get("/")
        model = apps.get_model("register", "PlantVariety")
        subtitle = "My subtitle"

        template_context = list_page_header(response.context, "register.PlantVariety", subtitle=subtitle)

        self.assertEqual(template_context["header"].page_title, model._meta.verbose_name_plural.title())
        self.assertEqual(template_context["header"].subtitle, subtitle)

    def test_list_page_header_uses_provided_title_and_subtitle(self):
        response = self.client.get("/")
        title = "Title"
        subtitle = "My subtitle"

        template_context = list_page_header(response.context, "register.PlantVariety", title=title, subtitle=subtitle)
        self.assertEqual(template_context["header"].page_title, title)
        self.assertEqual(template_context["header"].subtitle, subtitle)

    def test_list_page_header_fails_with_malformed_model_label(self):
        response = self.client.get("/")
        with self.assertRaises(TemplateSyntaxError):
            list_page_header(response.context, "not_a_model")


class AssetsTest(SimpleTestCase):
    def setUp(self):
        self.context = {}

    def test_assets_structure_is_ensured_in_context(self):
        assets = _ensure_assets(self.context)
        self.assertEqual({"css": [], "js": [], "hs": []}, assets)
        self.assertEqual({"template_assets": {"css": [], "js": [], "hs": []}}, self.context)
