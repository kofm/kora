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
