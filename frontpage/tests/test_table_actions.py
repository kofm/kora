from html.parser import HTMLParser
from urllib.parse import parse_qs, urlsplit

from django.contrib.auth.models import Permission
from django.test import TestCase
from django.urls import reverse

from calculator.factories import ManagementFactory, ManagementTypeFactory, ParameterObservationFactory
from frontpage.factories import UserFactory
from parameters.factories import ParameterFactory
from parameters.models import VarietalParameter
from register.factories import PlantSpeciesFactory, PlantVarietyFactory


class ActionMarkup(HTMLParser):
    def __init__(self, html):
        super().__init__()
        self.links = {}
        self.tooltips = []
        self.feed(html)

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if tag == "a" and "hx-get" in attrs:
            self.links[attrs["hx-get"]] = attrs
        if "title" in attrs:
            self.tooltips.append(attrs)


class EditDeleteActionsTests(TestCase):
    def test_list_actions_respect_independent_permissions_and_open_modals(self):
        records = (
            (ManagementTypeFactory(), "calculator:managementtype_list"),
            (ParameterFactory(), "parameters:parameter_list"),
            (PlantSpeciesFactory(), "register:plantspecies_list"),
        )
        for record, list_name in records:
            opts = record._meta
            for edit, delete in ((False, False), (True, False), (False, True), (True, True)):
                with self.subTest(model=opts.label, edit=edit, delete=delete):
                    user = UserFactory()
                    codenames = [f"view_{opts.model_name}"]
                    if edit:
                        codenames.append(f"change_{opts.model_name}")
                    if delete:
                        codenames.append(f"delete_{opts.model_name}")
                    user.user_permissions.add(
                        *Permission.objects.filter(content_type__app_label=opts.app_label, codename__in=codenames)
                    )
                    self.client.force_login(user)
                    response = self.client.get(reverse(list_name))
                    self.assertEqual(response.status_code, 200)
                    links = ActionMarkup(response.content.decode()).links
                    for url, allowed in ((record.get_update_url(), edit), (record.get_delete_url(), delete)):
                        self.assertEqual(url in links, allowed)
                        if allowed:
                            self.assertEqual(links[url]["hx-target"], "#modal")
                            self.assertEqual(links[url]["data-bs-toggle"], "modal")

    def test_varietal_parameter_actions_preserve_origin_for_refresh_or_redirect(self):
        self.client.force_login(UserFactory(is_superuser=True))
        reference = VarietalParameter.objects.create(
            variety=PlantVarietyFactory(), parameter=ParameterFactory(type="integer"), value_integer=1
        )
        origins = (
            f"{reverse('parameters:varietalparameter_list')}?parameter={reference.parameter_id}&page=1",
            f"{reverse('register:variety_detail', args=[reference.variety_id])}?para_page=1",
        )
        for origin in origins:
            with self.subTest(origin=origin):
                response = self.client.get(origin)
                self.assertEqual(response.status_code, 200)
                links = ActionMarkup(response.content.decode()).links
                for action_url in (reference.get_update_url(), reference.get_delete_url()):
                    url = next(url for url in links if urlsplit(url).path == action_url)
                    self.assertEqual(parse_qs(urlsplit(url).query)["next"], [origin])

    def test_protected_records_explain_disabled_delete_on_initial_and_htmx_lists(self):
        user = UserFactory(is_superuser=True)
        self.client.force_login(user)
        records = (
            (ManagementFactory().type, "calculator:managementtype_list"),
            (ParameterObservationFactory(created_by=user).parameter, "parameters:parameter_list"),
            (PlantVarietyFactory().species, "register:plantspecies_list"),
        )
        for record, list_name in records:
            for htmx in (False, True):
                with self.subTest(model=record._meta.label, htmx=htmx):
                    headers = {"HTTP_HX_REQUEST": "true"} if htmx else {}
                    response = self.client.get(reverse(list_name), **headers)
                    self.assertEqual(response.status_code, 200)
                    markup = ActionMarkup(response.content.decode())
                    self.assertNotIn(record.get_delete_url(), markup.links)
                    self.assertIn(record.get_update_url(), markup.links)
                    tooltip = next(t for t in markup.tooltips if t["title"] == record.cant_delete_msg)
                    self.assertIn("row-action", tooltip["class"].split())
                    self.assertEqual(tooltip["tabindex"], "0")
                    self.assertContains(response, 'aria-disabled="true"')
