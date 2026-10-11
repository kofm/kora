import json
from html.parser import HTMLParser

from django.contrib.auth.models import Permission
from django.db import connection
from django.test import TestCase
from django.test.utils import CaptureQueriesContext
from django.urls import reverse

from describe.factories import (
    DescriptionFactory,
    DescriptionLabelFactory,
    ExpressionFactory,
    ProtocolFactory,
    StateFactory,
    StateGroupFactory,
    TraitFactory,
    WorkspaceElementFactory,
    WorkspaceFactory,
)
from describe.models import Trait, WorkspaceElement
from frontpage.factories import UserFactory
from frontpage.testcases import ViewSmokeTestMixin
from register.factories import PlantSpeciesFactory, PlantVarietyFactory


class DescribeViewsSmokeTest(ViewSmokeTestMixin, TestCase):
    def setUp(self):
        self.app_name = "describe"
        self.user = UserFactory(is_superuser=True)
        self.client.force_login(self.user)
        self.description = DescriptionFactory()
        self.workspace = WorkspaceFactory(user=self.user)
        self.protocol = ProtocolFactory()
        WorkspaceElementFactory.create_batch(2, workspace=self.workspace)

    def test_description_views(self):
        self.assert_get(["description_list", "description_compare"])
        self.assert_get(["description_detail", "description_expression_update"], [self.description.id])
        self.assert_post(["description_delete"], [self.description.id], status_code=302)


class DescriptionCompareTests(TestCase):
    def test_species_protocol_sections_keep_columns_and_comparison_indicators(self):
        user = UserFactory()
        self.client.force_login(user)
        workspace = WorkspaceFactory(user=user)
        label = DescriptionLabelFactory(name="Reference", colour="blue")
        species = PlantSpeciesFactory(common_name="Comparison species A")
        protocol = ProtocolFactory(plantspecies=species, name="Primary protocol")
        varieties = [PlantVarietyFactory(species=species, name=name) for name in ("Alpha", "Beta")]
        descriptions = [
            DescriptionFactory(variety=variety, protocol=protocol, label=label) for variety in varieties
        ]
        for description in descriptions:
            WorkspaceElementFactory(workspace=workspace, description=description)

        differing = TraitFactory(protocol=protocol, numeric_id=1, description="Height", grouping=True)
        for description, name, code in zip(descriptions, ("Short", "Tall"), (1, 2), strict=True):
            state = StateFactory(trait=differing, numeric_id=code, description=name)
            ExpressionFactory(description=description, state=state)
        equal = TraitFactory(protocol=protocol, numeric_id=2, description="Colour", grouping=False)
        green = StateFactory(trait=equal, numeric_id=1, description="Green")
        for description in descriptions:
            ExpressionFactory(description=description, state=green)
        missing = TraitFactory(protocol=protocol, numeric_id=3, description="Shape", grouping=False)
        round_state = StateFactory(trait=missing, numeric_id=1, description="Round")
        ExpressionFactory(description=descriptions[0], state=round_state)

        # A second protocol is included for the same variety/label even when not saved in the workspace.
        other_protocol = ProtocolFactory(plantspecies=species, name="Secondary protocol")
        other_description = DescriptionFactory(variety=varieties[0], protocol=other_protocol, label=label)
        other_trait = TraitFactory(protocol=other_protocol, numeric_id=1, description="Width", grouping=False)
        wide = StateFactory(trait=other_trait, numeric_id=1, description="Wide")
        ExpressionFactory(description=other_description, state=wide)

        other_species = PlantSpeciesFactory(common_name="Comparison species B")
        third_protocol = ProtocolFactory(plantspecies=other_species, name="Other species protocol")
        third_description = DescriptionFactory(
            variety=PlantVarietyFactory(species=other_species, name="Gamma"), protocol=third_protocol, label=label
        )
        WorkspaceElementFactory(workspace=workspace, description=third_description)
        third_trait = TraitFactory(protocol=third_protocol, numeric_id=1, description="Texture", grouping=False)
        smooth = StateFactory(trait=third_trait, numeric_id=1, description="Smooth")
        ExpressionFactory(description=third_description, state=smooth)

        response = self.client.get(reverse("describe:description_compare"))
        self.assertContains(response, species.common_name)
        self.assertContains(response, other_species.common_name)
        self.assertContains(response, 'badge rounded-pill label-blue', count=3)

        class ComparisonParser(HTMLParser):
            def __init__(self):
                super().__init__()
                self.tables = []
                self.table = None
                self.cell = None

            def handle_starttag(self, tag, attrs):
                attrs = dict(attrs)
                if tag == "table" and "description-comparison-table" in attrs.get("class", "").split():
                    self.table = []
                    self.tables.append(self.table)
                elif self.table is not None:
                    if tag == "tr":
                        self.cells = []
                        self.table.append((attrs.get("class", "").split(), self.cells))
                    elif tag in ("td", "th"):
                        self.cell = []

            def handle_data(self, data):
                if self.cell is not None:
                    self.cell.append(data)

            def handle_endtag(self, tag):
                if tag in ("td", "th") and self.cell is not None:
                    self.cells.append(" ".join("".join(self.cell).split()))
                    self.cell = None
                elif tag == "table":
                    self.table = None

        parser = ComparisonParser()
        parser.feed(response.content.decode())
        self.assertEqual(len(parser.tables), 2)
        first, second = parser.tables
        self.assertEqual([cells for _, cells in first], [
            ["Trait", "Alpha Reference", "Beta Reference"],
            ["Primary protocol", ""],
            ["1. Height ✱", "1. Short", "2. Tall"],
            ["2. Colour", "1. Green", "1. Green"],
            ["3. Shape", "1. Round", "—"],
            ["Secondary protocol", ""],
            ["1. Width", "1. Wide", "—"],
        ])
        self.assertIn("description-comparison-different", first[2][0])
        self.assertIn("fw-bold", first[2][0])
        for index in (3, 4, 6):
            self.assertNotIn("description-comparison-different", first[index][0])
        self.assertEqual([cells for _, cells in second], [
            ["Trait", "Gamma Reference"],
            ["Other species protocol", ""],
            ["1. Texture", "1. Smooth"],
        ])

        # A repeated pair from another protocol must not introduce a column;
        # every protocol's cells must follow the reordered sidebar columns.
        WorkspaceElement.objects.filter(description=descriptions[0]).update(order=2)
        WorkspaceElement.objects.filter(description=descriptions[1]).update(order=1)
        WorkspaceElementFactory(workspace=workspace, description=other_description, order=3)
        response = self.client.get(
            reverse("describe:description_compare"), {"partial": "comparison"}, HTTP_HX_REQUEST="true"
        )
        reordered = ComparisonParser()
        reordered.feed(response.content.decode())
        self.assertEqual([cells for _, cells in reordered.tables[0]], [
            ["Trait", "Beta Reference", "Alpha Reference"],
            ["Primary protocol", ""],
            ["1. Height ✱", "2. Tall", "1. Short"],
            ["2. Colour", "1. Green", "1. Green"],
            ["3. Shape", "—", "1. Round"],
            ["Secondary protocol", ""],
            ["1. Width", "—", "1. Wide"],
        ])

    def test_empty_comparison_stays_available_for_sidebar_interactions(self):
        user = UserFactory()
        self.client.force_login(user)
        url = reverse("describe:description_compare")
        workspace = WorkspaceFactory(user=user, is_active=False)
        for active in (False, True):
            workspace.is_active = active
            workspace.save()
            for partial in (None, "comparison"):
                response = (
                    self.client.get(url, {"partial": partial}, HTTP_HX_REQUEST="true")
                    if partial else self.client.get(url)
                )
                self.assertContains(response, "This workspace is empty" if active else "No workspace is active")

    def test_sidebar_mutations_refresh_the_correct_comparison_regions(self):
        user = UserFactory(is_superuser=True)
        self.client.force_login(user)
        WorkspaceFactory(user=user)
        other = WorkspaceFactory(user=user, is_active=False)
        headers = {"HTTP_HX_REQUEST": "true"}

        def mutate(name, data=None, pk=None, events=()):
            response = self.client.post(reverse(f"describe:{name}", args=[pk] if pk else None), data or {}, **headers)
            self.assertEqual(response.status_code, 200)
            self.assertEqual(set(json.loads(response.headers.get("HX-Trigger", "{}"))), set(events))
            return response

        both = ("workspaceChanged", "workspaceElementsChanged")
        mutate("workspace_activate", {"workspace": other.pk}, events=both)
        mutate("workspace_activate", {"workspace": other.pk})
        mutate("workspace_update", {"name": "Renamed workspace"}, other.pk, ("workspaceChanged",))
        response = self.client.get(reverse("describe:description_compare"), {"partial": "breadcrumbs"}, **headers)
        self.assertContains(response, "Renamed workspace")
        mutate("workspace_update", {"name": "Renamed workspace"}, other.pk)
        element = WorkspaceElementFactory(workspace=other)
        mutate("workspace_sort", {"order": [element.pk]}, events=("workspaceElementsChanged",))
        mutate("workspace_element_delete", pk=element.pk, events=("workspaceElementsChanged",))
        response = self.client.get(reverse("describe:description_compare"), {"partial": "comparison"}, **headers)
        self.assertContains(response, "This workspace is empty")
        mutate("workspace_delete", pk=other.pk, events=both)
        response = self.client.get(reverse("describe:description_compare"), {"partial": "header"}, **headers)
        self.assertContains(response, "No active workspace")
        mutate("workspace_create", {"name": "Created workspace"}, events=both)
        mutate("workspace_activate", {"workspace": ""}, events=both)


class FindSimilarTests(TestCase):
    def setUp(self):
        self.client.force_login(UserFactory(is_superuser=True))
        self.description = DescriptionFactory()
        self.url = reverse("describe:description_find_similar")

    def make_trait(self, codes, *, grouping=True, expression_type="QN"):
        trait = TraitFactory(
            protocol=self.description.protocol,
            grouping=grouping,
            type_of_expression=expression_type,
        )
        states = [StateFactory(trait=trait, numeric_id=code) for code in codes]
        return trait, states

    def record(self, *states):
        for state in states:
            ExpressionFactory(description=self.description, state=state)

    def assert_selections(self, expected, *, htmx=False):
        headers = {"HTTP_HX_REQUEST": "true"} if htmx else {}
        response = self.client.get(self.url, {"description_id": self.description.pk}, **headers)
        self.assertEqual(response.status_code, 200 if htmx else 302)
        session_filter = self.client.session["description_filter"]
        self.assertEqual(session_filter["expressions"], expected)
        self.assertEqual(session_filter["protocol"], self.description.protocol_id)
        if htmx:

            class CheckedInputs(HTMLParser):
                def __init__(self):
                    super().__init__()
                    self.values = set()

                def handle_starttag(self, tag, attrs):
                    attrs = dict(attrs)
                    if tag == "input" and "checked" in attrs and attrs.get("name", "").endswith("-expressions"):
                        self.values.add(int(attrs["value"]))

            parser = CheckedInputs()
            parser.feed(response.content.decode())
            self.assertEqual(parser.values, {pk for states in expected.values() for pk in states})
        else:
            self.assertEqual(response.url, reverse("describe:description_list") + "?reset=false")

    def test_quantitative_neighbors_follow_available_codes_and_stop_at_boundaries(self):
        trait, states = self.make_trait([1, 3, 5, 7, 9])
        for index, neighbors in ((0, states[:2]), (2, states[1:4]), (4, states[3:])):
            self.description.expressions.all().delete()
            self.record(states[index])
            expected = {str(trait.pk): [state.pk for state in neighbors]}
            for htmx in (False, True):
                with self.subTest(code=states[index].numeric_id, htmx=htmx):
                    self.assert_selections(expected, htmx=htmx)

    def test_only_grouping_quantitative_traits_are_expanded(self):
        expected = {}
        for expression_type in ("QN", "QL", "PQ", ""):
            trait, states = self.make_trait([4, 5, 6], expression_type=expression_type)
            self.record(states[1])
            selected = states if expression_type == "QN" else states[1:2]
            expected[str(trait.pk)] = [state.pk for state in selected]
        _, non_grouping_states = self.make_trait([4, 5, 6], grouping=False)
        self.record(non_grouping_states[1])
        self.assert_selections(expected, htmx=True)

    def test_multiple_recorded_states_combine_overlapping_neighbors(self):
        trait, states = self.make_trait([1, 3, 5, 7, 9])
        self.record(states[1], states[2])
        self.assert_selections({str(trait.pk): [state.pk for state in states[:4]]})


class WorkspaceSidebarTests(TestCase):
    def setUp(self):
        self.user = UserFactory(is_superuser=True)
        self.client.force_login(self.user)
        self.workspace = WorkspaceFactory(user=self.user)
        self.url = reverse("describe:workspace_detail")

    def test_labels_are_coloured_and_optional(self):
        label = DescriptionLabelFactory(name="Sidebar reference", colour="blue")
        protocol = ProtocolFactory(name="Sidebar protocol")
        for description_label in (label, None):
            WorkspaceElementFactory(
                workspace=self.workspace,
                description=DescriptionFactory(protocol=protocol, label=description_label),
            )

        response = self.client.get(self.url)

        self.assertContains(response, "Sidebar protocol", count=2)
        self.assertContains(
            response,
            '<span class="badge rounded-pill label-blue ms-1">Sidebar reference</span>',
            html=True,
        )
        self.assertContains(response, 'class="badge rounded-pill', count=1)

    def test_rendering_more_labels_does_not_add_per_item_queries(self):
        def add_element(index):
            label = DescriptionLabelFactory(name=f"Sidebar label {index}")
            WorkspaceElementFactory(
                workspace=self.workspace,
                description=DescriptionFactory(label=label),
            )

        add_element(0)
        with CaptureQueriesContext(connection) as small_workspace:
            response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

        for index in range(1, 5):
            add_element(index)
        with self.assertNumQueries(len(small_workspace)):
            response = self.client.get(self.url)
        for index in range(5):
            self.assertContains(response, f"Sidebar label {index}")


class WorkspaceOwnershipTests(TestCase):
    def setUp(self):
        self.user = UserFactory()
        self.other_user = UserFactory()
        self.workspace = WorkspaceFactory(user=self.other_user, name="Private workspace")
        self.element = WorkspaceElementFactory(workspace=self.workspace, order=4)
        self.client.force_login(self.user)

    def grant(self, *codenames):
        self.user.user_permissions.add(*(Permission.objects.get(codename=codename) for codename in codenames))

    def test_update_and_delete_hide_another_users_workspace(self):
        self.grant("change_workspace", "delete_workspace")

        update_response = self.client.post(
            reverse("describe:workspace_update", args=[self.workspace.pk]),
            {"name": "Taken over"},
        )
        delete_response = self.client.post(reverse("describe:workspace_delete", args=[self.workspace.pk]))

        self.assertEqual(update_response.status_code, 404)
        self.assertEqual(delete_response.status_code, 404)
        self.workspace.refresh_from_db()
        self.assertEqual(self.workspace.name, "Private workspace")
        self.assertEqual(self.workspace.user, self.other_user)

    def test_sort_rejects_mixed_ownership_without_partial_updates(self):
        own_workspace = WorkspaceFactory(user=self.user)
        own_element = WorkspaceElementFactory(workspace=own_workspace, order=7)
        self.grant("change_workspaceelement")

        response = self.client.post(
            reverse("describe:workspace_sort"),
            {"order": [own_element.pk, self.element.pk]},
        )

        self.assertEqual(response.status_code, 400)
        own_element.refresh_from_db()
        self.element.refresh_from_db()
        self.assertEqual(own_element.order, 7)
        self.assertEqual(self.element.order, 4)


class BulkWorkspaceResultsTests(TestCase):
    def setUp(self):
        self.user = UserFactory(is_superuser=True)
        self.client.force_login(self.user)
        self.workspace = WorkspaceFactory(user=self.user)
        self.protocol = ProtocolFactory()
        self.url = reverse("describe:workspace_elements_add_results")
        self.label = DescriptionLabelFactory(name="Bulk results label")

    def set_filter(self, **overrides):
        session = self.client.session
        session["description_filter"] = {
            "protocol": self.protocol.pk,
            "strict": False,
            "label": [],
            "expressions": {},
            **overrides,
        }
        session.save()

    def test_all_pages_use_every_filter_and_append_sorted_without_duplicates(self):
        state = StateFactory(trait__protocol=self.protocol)
        matches = [
            DescriptionFactory(protocol=self.protocol, label=self.label, variety__name=f"zz {index:02}")
            for index in range(12)
        ]
        label = matches[0].label
        for description in matches:
            ExpressionFactory(description=description, state=state)

        # Each excluded description violates just one of the effective filters.
        excluded = [
            DescriptionFactory(label=label, variety__name="zz other protocol"),
            DescriptionFactory(protocol=self.protocol, label=None, variety__name="zz other label"),
            DescriptionFactory(protocol=self.protocol, label=label, variety__name="zz missing expression"),
            DescriptionFactory(protocol=self.protocol, label=label, variety__name="unrelated"),
        ]
        for description in (excluded[0], excluded[1], excluded[3]):
            ExpressionFactory(description=description, state=state)
        existing = WorkspaceElementFactory(workspace=self.workspace, description=matches[0], order=7)
        other_workspace = WorkspaceFactory(user=UserFactory())
        self.set_filter(strict=True, label=[label.pk], expressions={str(state.trait_id): [state.pk]})
        params = {"variety": "zz", "sort": "-variety__name", "page": 1}

        response = self.client.post(self.url, query_params=params)

        self.assertEqual(response.status_code, 302)
        expected = [matches[0].pk] + [description.pk for description in reversed(matches[1:])]
        self.assertEqual(list(self.workspace.descriptions.values_list("description_id", flat=True)), expected)
        self.assertEqual(list(self.workspace.descriptions.values_list("order", flat=True)), list(range(7, 19)))
        self.assertFalse(other_workspace.descriptions.exists())
        existing.refresh_from_db()
        self.assertEqual(existing.order, 7)
        # A repeated HTMX click must neither duplicate nor reorder membership.
        self.client.post(self.url, query_params=params, HTTP_HX_REQUEST="true")
        self.assertEqual(list(self.workspace.descriptions.values_list("description_id", flat=True)), expected)

    def test_protocol_alone_is_not_filtering_but_variety_search_is(self):
        match = DescriptionFactory(protocol=self.protocol, label=self.label, variety__name="zz match")
        DescriptionFactory(protocol=self.protocol, label=self.label, variety__name="unrelated")
        self.set_filter()
        response = self.client.post(self.url, HTTP_HX_REQUEST="true")
        self.assertEqual(response.status_code, 400)
        self.assertFalse(self.workspace.descriptions.exists())
        list_url = reverse("describe:description_list")
        response = self.client.get(list_url, {"reset": "false"})
        self.assertNotContains(response, 'title="Add all results to active workspace"')
        response = self.client.get(list_url, {"reset": "false", "variety": "zz"})
        self.assertContains(response, 'title="Add all results to active workspace"')
        self.assertContains(response, "Add all 1 matching descriptions")
        self.client.post(self.url, query_params={"variety": "zz"})
        self.assertEqual(list(self.workspace.descriptions.values_list("description_id", flat=True)), [match.pk])

    def test_no_owned_active_workspace_does_not_use_another_users_workspace(self):
        self.workspace.is_active = False
        self.workspace.save()
        other_workspace = WorkspaceFactory(user=UserFactory())
        DescriptionFactory(protocol=self.protocol, label=self.label)
        self.set_filter(strict=True)

        response = self.client.post(self.url, HTTP_HX_REQUEST="true")

        self.assertEqual(response.headers["HX-Reswap"], "none")
        self.assertFalse(WorkspaceElement.objects.filter(workspace__in=[self.workspace, other_workspace]).exists())


class TraitExpressionTypeTests(TestCase):
    def test_editor_creates_unspecified_trait_and_can_set_and_clear_expression_type(self):
        self.client.force_login(UserFactory(is_superuser=True))
        protocol = ProtocolFactory()
        data = {"numeric_id": 1, "description": "Leaf colour", "protocol": protocol.pk}

        response = self.client.post(reverse("describe:trait_create", args=[protocol.pk]), data)
        self.assertEqual(response.status_code, 302)
        trait = Trait.objects.get(protocol=protocol, numeric_id=1)
        self.assertEqual(trait.type_of_expression, "")
        url = reverse("describe:trait_update", args=[trait.pk])
        self.assertContains(self.client.get(url), 'name="type_of_expression"')

        data.update({"states-TOTAL_FORMS": 0, "states-INITIAL_FORMS": 0})
        for expression_type in ("QL", "QN", "PQ", ""):
            with self.subTest(expression_type=expression_type):
                response = self.client.post(url, {**data, "type_of_expression": expression_type})
                self.assertEqual(response.status_code, 200)
                trait.refresh_from_db()
                self.assertEqual(trait.type_of_expression, expression_type)


class TraitAutocompleteTests(TestCase):
    def test_filters_traits_by_protocol(self):
        self.client.force_login(UserFactory())
        protocol = ProtocolFactory()
        matching_trait = TraitFactory(protocol=protocol)
        other_trait = TraitFactory(protocol=ProtocolFactory())

        response = self.client.get(reverse("describe:trait_autocomplete"), {"protocol_id": protocol.pk})

        result_ids = {result["id"] for result in response.json()["results"]}
        self.assertEqual(result_ids, {matching_trait.pk})
        self.assertNotIn(other_trait.pk, result_ids)


class StateAutocompleteTests(TestCase):
    def test_filters_states_by_trait(self):
        self.client.force_login(UserFactory())
        trait = TraitFactory()
        matching_state = StateFactory(trait=trait)
        other_state = StateFactory(trait=TraitFactory())

        response = self.client.get(reverse("describe:state_autocomplete"), {"trait_id": trait.pk})

        result_ids = {result["id"] for result in response.json()["results"]}
        self.assertEqual(result_ids, {matching_state.pk})
        self.assertNotIn(other_state.pk, result_ids)


class StateDeleteTests(TestCase):
    def setUp(self):
        self.user = UserFactory(is_superuser=True)
        self.client.force_login(self.user)

    def test_deleting_articulation_state_preserves_and_regroups_remaining_states(self):
        group = StateGroupFactory()
        state_a = StateFactory(group=group)
        state_b = StateFactory(group=group)
        state_c = StateFactory(group=group)
        state_a.related_states.add(state_b)
        state_b.related_states.add(state_c)

        response = self.client.post(reverse("describe:state_delete", args=(state_b.pk,)))

        self.assertEqual(response.status_code, 302)
        self.assertFalse(type(state_b).objects.filter(pk=state_b.pk).exists())
        state_a.refresh_from_db()
        state_c.refresh_from_db()
        self.assertNotEqual(state_a.group_id, state_c.group_id)
