from datetime import timedelta

from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from describe.factories import DescriptionFactory, StateFactory, TraitFactory
from describe.models import Description, Expression
from frontpage.factories import UserFactory


class ExpressionTimestampTests(TestCase):
    def setUp(self):
        self.client.force_login(UserFactory(is_superuser=True))
        self.description = DescriptionFactory()
        self.trait = TraitFactory(protocol=self.description.protocol)
        self.state = StateFactory(trait=self.trait)
        self.old_timestamp = timezone.now() - timedelta(days=1)
        self.created_at = self.description.created_at

    def reset_timestamp(self):
        Description.objects.filter(pk=self.description.pk).update(updated_at=self.old_timestamp)

    def assert_description_updated(self):
        self.description.refresh_from_db()
        self.assertGreater(self.description.updated_at, self.old_timestamp)
        self.assertEqual(self.description.created_at, self.created_at)

    def test_expression_creation_updates_description(self):
        self.reset_timestamp()
        response = self.client.post(
            reverse("describe:expression-create"),
            {"description": self.description.pk, "trait": self.trait.pk, "state": self.state.pk, "note": ""},
        )
        self.assertEqual(response.status_code, 200)
        self.assertTrue(Expression.objects.filter(description=self.description, state=self.state).exists())
        self.assert_description_updated()

    def test_state_and_note_edits_update_description(self):
        expression = Expression.objects.create(description=self.description, state=self.state, note="original")
        other_state = StateFactory(trait=self.trait)
        for state, note in ((other_state, "original"), (other_state, "edited")):
            with self.subTest(state=state.pk, note=note):
                self.reset_timestamp()
                response = self.client.post(
                    reverse("describe:expression-update", args=[expression.pk]),
                    {"description": self.description.pk, "state": state.pk, "note": note},
                )
                self.assertEqual(response.status_code, 200)
                expression.refresh_from_db()
                self.assertEqual(expression.state_id, state.pk)
                self.assertEqual(expression.note, note)
                self.assert_description_updated()

    def test_expression_deletion_updates_description(self):
        expression = Expression.objects.create(description=self.description, state=self.state)
        self.reset_timestamp()
        response = self.client.post(reverse("describe:expression-delete", args=[expression.pk]))
        self.assertEqual(response.status_code, 200)
        self.assertFalse(Expression.objects.filter(pk=expression.pk).exists())
        self.assert_description_updated()

    def test_bulk_api_creation_updates_only_affected_descriptions(self):
        other = DescriptionFactory(protocol=self.description.protocol)
        untouched = DescriptionFactory(protocol=self.description.protocol)
        Description.objects.filter(pk__in=[self.description.pk, other.pk, untouched.pk]).update(
            updated_at=self.old_timestamp
        )
        other_created_at = other.created_at
        response = self.client.post(
            reverse("restapi:expressions-bulk"),
            [
                {"description": self.description.pk, "state": self.state.pk, "note": "first"},
                {"description": other.pk, "state": self.state.pk, "note": "second"},
                {"description": self.description.pk, "state": self.state.pk, "note": "third"},
            ],
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 201)
        self.assertEqual(Expression.objects.count(), 3)
        self.assert_description_updated()
        other.refresh_from_db()
        untouched.refresh_from_db()
        self.assertGreater(other.updated_at, self.old_timestamp)
        self.assertEqual(other.created_at, other_created_at)
        self.assertEqual(untouched.updated_at, self.old_timestamp)
