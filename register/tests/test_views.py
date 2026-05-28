import json

from django.contrib.auth.models import Permission, User
from django.test import RequestFactory, SimpleTestCase, TestCase
from django.urls import reverse
from factory.declarations import Iterator

from frontpage.autocomplete import AutocompleteModelView
from frontpage.factories import AdminFactory
from register.factories import PlantSpeciesFactory, PlantVarietyFactory
from register.filters import TRIGRAM_SEARCH_THRESHOLD, PlantVarietyFilter, filter_name_generic
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
        self.assertTemplateUsed(response, "frontpage/modal_form.html")
        self.assertIn("object_to_create", response.context)

    def test_post_creates_plantvariety(self):
        self.client.login(username="permuser", password="password")
        response = self.client.post(
            self.create_url,
            {"name": "Cherry Tomato", "species": self.species.pk},
        )
        self.assertEqual(response.status_code, 200)
        self.assertTrue(PlantVariety.objects.filter(name="Cherry Tomato").exists())


class FilterNameGenericTest(SimpleTestCase):
    def setUp(self):
        class FakeQS:
            def __init__(self):
                self.filters = []
                self.annotations = []
                self.ordering = []

            def filter(self, **kwargs):
                self.filters.append(kwargs)
                return self

            def annotate(self, **kwargs):
                self.annotations.append(kwargs)
                return self

            def order_by(self, *fields):
                self.ordering = list(fields)
                return self

        self.FakeQS = FakeQS
        self.qs = FakeQS()

    def test_query_annotations(self):
        filter_name_generic(self.qs, "names__name", "foobarbaz")
        self.assertGreaterEqual(len(self.qs.annotations), 2)
        annotated_fields = set().union(*self.qs.annotations)
        self.assertIn("search_name", annotated_fields)
        self.assertIn("similarity", annotated_fields)
        self.assertIn("rank", annotated_fields)

    def test_query_ordering(self):
        filter_name_generic(self.qs, "names__name", "foobarbaz")
        self.assertEqual(self.qs.ordering, ["rank", "-similarity", "search_name"])

    def test_short_query_uses_icontains(self):
        result = filter_name_generic(self.qs, "names__name", "foobarbaz"[0 : TRIGRAM_SEARCH_THRESHOLD - 1])

        self.assertIs(result, self.qs)
        self.assertEqual(len(self.qs.filters), 1)
        self.assertTrue(any("search_name__icontains" in f for f in self.qs.filters))

    def test_long_query_uses_trigramsimilarity(self):
        result = filter_name_generic(self.qs, "names__name", "foobarbaz"[0:TRIGRAM_SEARCH_THRESHOLD])

        self.assertIs(result, self.qs)
        self.assertEqual(len(self.qs.filters), 1)
        self.assertTrue(any("similarity__gt" in f for f in self.qs.filters))

    def test_empty_value_returns_original_queryset(self):
        qs = self.FakeQS()
        result = filter_name_generic(qs, "names__name", "")
        self.assertIs(result, qs)
        self.assertEqual(self.qs.filters, [])
        self.assertEqual(self.qs.annotations, [])
        self.assertEqual(self.qs.ordering, [])


class RegisterViewsSmokeTest(TestCase):
    def setUp(self) -> None:
        self.user = AdminFactory(username="tester", password="pass")
        self.client.login(username="tester", password="pass")

    def test_variety_list_view(self):
        response = self.client.get(reverse("register:variety_list"))
        self.assertEqual(response.status_code, 200)


class PlantVarietyFilterTest(TestCase):
    def setUp(self) -> None:
        species = PlantSpeciesFactory()
        self.varieties = PlantVarietyFactory.create_batch(
            4,
            name=Iterator(
                [
                    "Carnaroli",
                    "Carnarolo",
                    "Foo",
                    "Carnarole",
                ]
            ),
            species=species,
        )

    def apply_filter(self, params):
        qs = PlantVariety.objects.all()
        f = PlantVarietyFilter(params, queryset=qs)
        return f.qs

    def test_variety_filter_exact_match_is_first(self):
        result = self.apply_filter({"name": "carnaroli"})
        variety_names = [obj.name for obj in result]
        self.assertEqual("Carnaroli", variety_names[0])

    def test_variety_filter_non_matching_varieties(self):
        result = self.apply_filter({"name": "carnaroli"})
        variety_names = [obj.name for obj in result]
        self.assertIn("Carnaroli", variety_names)
        self.assertIn("Carnarole", variety_names)
        self.assertIn("Carnarolo", variety_names)
        self.assertNotIn("Foo", variety_names)


class TestAutocompleteView(AutocompleteModelView):
    model = PlantVariety
    filter_by = ["species_id"]
    ordering = ["pk"]


class AutocompleteViewTest(TestCase):
    def setUp(self) -> None:
        self.factory = RequestFactory()
        PlantVarietyFactory.create_batch(4)
        self.varieties = PlantVariety.objects.order_by("pk")

    def test_get_returns_json_response(self):
        request = self.factory.get("/autocomplete/?q=")

        response = TestAutocompleteView.as_view()(request)
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertEqual(len(data["results"]), 4)
        check = [{"id": obj.pk, "name": obj.name, "text": str(obj)} for obj in self.varieties]
        self.assertEqual(check, data["results"])

    def test_get_returns_json_response_filtered(self):
        species_id = self.varieties[0].species_id
        request = self.factory.get(f"/autocomplete/?q=&species_id={species_id}")

        response = TestAutocompleteView.as_view()(request)
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        check = [
            {"id": obj.pk, "name": obj.name, "text": str(obj)} for obj in self.varieties if obj.species_id == species_id
        ]
        self.assertEqual(check, data["results"])
