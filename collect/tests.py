from django.core.exceptions import ValidationError
from django.db import IntegrityError
from django.test import TestCase
from django.utils import timezone
from factory.declarations import Iterator

from collect.exceptions import SampleDiscardError
from collect.factories import CartFactory, CartItemFactory, SampleFactory, SampleWeightFactory
from collect.models import CartKind, Sample, SampleStatus


class SampleTests(TestCase):
    def setUp(self):
        self.samples = SampleFactory.create_batch(3)
        s2 = self.samples[2]
        SampleWeightFactory(sample=s2, weight=10)
        self.cartitem = CartItemFactory(sample=s2)

    def test_sample_id_unique_validation_sees_discarded(self):
        s = self.samples[0]
        s.discard()
        s.refresh_from_db()

        s2 = SampleFactory.build(sample_id=s.sample_id)
        with self.assertRaises(ValidationError):
            s2.full_clean()

    def test_samples_are_created_active(self):
        self.assertTrue(all(s.status == SampleStatus.ACTIVE for s in self.samples))
        self.assertTrue(all(s.discarded_at is None for s in self.samples))

    def test_sample_are_discarded(self):
        s = self.samples[0]
        s.discard()
        s.refresh_from_db()

        self.assertEqual(s.status, SampleStatus.DISCARDED)
        self.assertIsNotNone(s.discarded_at)

    def test_samples_status_discarded_at_constraints(self):
        s = self.samples[0]
        s.status = SampleStatus.DISCARDED
        with self.assertRaises(IntegrityError):
            s.save()

    def test_default_sample_manager_returns_only_active(self):
        s0 = self.samples[0]
        s0.discard()
        qs = Sample.objects.all()
        self.assertEqual(qs.count(), 2)
        self.assertFalse(qs.filter(pk=s0.pk).exists())

    def test_samples_are_bulk_discarded_if_not_referenced_by_any_cartitem(self):
        Sample.objects.all().discard()
        self.assertTrue(Sample.objects.exists())  # The Sample referenced by CartItem is not deleted
        self.assertEqual(Sample.objects.count(), 1)

    def test_samples_in_cart_are_not_discarded(self):
        s2 = self.samples[2]
        with self.assertRaises(SampleDiscardError) as e:
            s2.discard()
        self.assertEqual(e.exception.code, "in_cart")

        s2.refresh_from_db()
        self.assertEqual(s2.status, SampleStatus.ACTIVE)
        self.assertIsNone(s2.discarded_at)

    def test_sample_status_position_invariant(self):
        s1 = self.samples[1]
        s1.status = SampleStatus.DISCARDED
        s1.discarded_at = timezone.now()
        with self.assertRaises(IntegrityError):
            s1.save()


class CartItemDiscardTests(TestCase):
    def setUp(self):
        self.cart1 = CartFactory()
        self.cart2 = CartFactory(kind=CartKind.DISCARD)
        self.samples = SampleFactory.create_batch(3)
        SampleWeightFactory.create_batch(3, sample=Iterator(self.samples), weight=100)
        CartItemFactory(cart=self.cart1, sample=self.samples[0])
        CartItemFactory.create_batch(3, cart=self.cart2, sample=Iterator(self.samples), weight=None)

    def test_cart_discard_only_if_not_referenced_by_any_cartitem(self):
        self.cart2.discard()
        self.assertEqual(self.cart2.cartitem_set.count(), 1)


class CartItemCleanTests(TestCase):
    def test_clean_fails_when_weight_exceeds_available(self):
        sample = SampleFactory()
        SampleWeightFactory(sample=sample, weight=10)
        CartItemFactory(sample=sample, weight=8)

        cart_item = CartItemFactory.build(sample=sample, weight=5)

        with self.assertRaises(ValidationError) as ctx:
            cart_item.clean()

        self.assertIn("weight", ctx.exception.message_dict)

    def test_clean_passes_when_weight_is_available(self):
        sample = SampleFactory()
        SampleWeightFactory(sample=sample, weight=10)
        CartItemFactory(sample=sample, weight=5)

        cart_item = CartItemFactory.build(sample=sample, weight=5)

        try:
            cart_item.clean()
        except ValidationError:
            self.fail("CartItem.clean() raised ValidationError unexpectedly.")

    def test_clean_allows_self_exclusion_from_reserved(self):
        """
        Scenario:
        - Total available: *10g*
        - CartItem A exists and has 4g reserved
        - User wants to edit A to reserve 10g

        If we don’t exclude A’s current reservation, the system sees:

        - Already reserved = 4g
        - New request = 10g ➡️ Total = 14g — would wrongly look like 4 + 10 = 14 , triggering a false-positive failure.

        So we need to exclude CartItem A from its own reservation.
        """
        sample = SampleFactory()
        SampleWeightFactory(sample=sample, weight=10)

        cart_item = CartItemFactory(sample=sample, weight=4)

        cart_item.weight = 10

        cart_item.clean()

    def test_clean_fails_if_increase_exceeds_available_even_with_exclusion(self):
        sample = SampleFactory()
        SampleWeightFactory(sample=sample, weight=10)
        cart_item = CartItemFactory(sample=sample, weight=4)
        CartItemFactory(sample=sample, weight=3)  # Another reservation

        cart_item.weight = 8  # Trying to go from 4g → 8g
        # Available: 10 - 3 = 7g (excluding self)

        with self.assertRaises(ValidationError):
            cart_item.clean()
