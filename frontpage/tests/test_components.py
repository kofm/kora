from django.apps import apps
from django.template import TemplateSyntaxError
from django.test import TestCase

from frontpage.factories import AdminFactory
from frontpage.templatetags.components import detail_page_header, list_page_header


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


class DetailPageHeaderTests(TestCase):
    def setUp(self):
        self.user = AdminFactory(username="tester", password="pass")
        self.client.login(username="tester", password="pass")

    def test_detail_page_header_exposes_primary_key_only_when_enabled(self):
        response = self.client.get("/")

        default_context = detail_page_header(response.context, self.user)
        enabled_context = detail_page_header(response.context, self.user, show_id=True)

        self.assertIsNone(default_context["object_id"])
        self.assertEqual(enabled_context["object_id"], self.user.pk)
