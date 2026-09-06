from django.contrib.auth.models import Permission
from django.test import TestCase
from django.urls import reverse

from describe.factories import (
    DescriptionFactory,
    ProtocolFactory,
    StateFactory,
    StateGroupFactory,
    TraitFactory,
    WorkspaceElementFactory,
    WorkspaceFactory,
)
from frontpage.factories import UserFactory
from frontpage.testcases import ViewSmokeTestMixin


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
