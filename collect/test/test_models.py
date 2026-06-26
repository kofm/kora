from django.core.exceptions import ValidationError
from django.db import IntegrityError
from django.db.models.deletion import ProtectedError
from django.test import TestCase
from django.utils import timezone
from factory.declarations import Iterator

from collect.exceptions import SampleDiscardError
from collect.factories import CartFactory, CartItemFactory, SampleFactory, SampleWeightFactory, StorageFactory
from collect.models import CartKind, Sample, SampleStatus, Storage, StoragePosition


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


class StoragePositionTests(TestCase):
    @classmethod
    def setUp(self):
        self.storage: Storage = StorageFactory()

    def test_set_positions_creates_positions_in_sequence_when_value_is_higher(self):
        self.storage.set_positions(5)

        self.assertEqual(self.storage.total_positions, 5)
        self.assertEqual(
            list(StoragePosition.objects.filter(storage=self.storage).order_by("name").values_list("name", flat=True)),
            [1, 2, 3, 4, 5],
        )

    def test_set_positions_removes_positions_greater_than_value_when_value_is_lower(self):
        self.storage.set_positions(5)

        self.storage.set_positions(2)

        self.assertEqual(self.storage.total_positions, 2)
        self.assertEqual(
            list(StoragePosition.objects.filter(storage=self.storage).order_by("name").values_list("name", flat=True)),
            [1, 2],
        )

    def test_set_positions_is_idempotent_for_same_value(self):
        self.storage.set_positions(3)
        first_position_ids = list(
            StoragePosition.objects.filter(storage=self.storage).order_by("name").values_list("id", flat=True)
        )

        self.storage.set_positions(3)

        self.assertEqual(self.storage.total_positions, 3)
        self.assertEqual(
            list(StoragePosition.objects.filter(storage=self.storage).order_by("name").values_list("id", flat=True)),
            first_position_ids,
        )

    def test_set_positions_can_grow_after_shrink(self):
        self.storage.set_positions(5)
        self.storage.set_positions(2)

        self.storage.set_positions(4)

        self.assertEqual(self.storage.total_positions, 4)
        self.assertEqual(
            list(StoragePosition.objects.filter(storage=self.storage).order_by("name").values_list("name", flat=True)),
            [1, 2, 3, 4],
        )

    def test_set_positions_can_shrink_to_highest_stored_position(self):
        self.storage.set_positions(5)
        protected_position = StoragePosition.objects.get(storage=self.storage, name=3)
        SampleFactory(position=protected_position)

        self.storage.set_positions(3)

        self.assertEqual(self.storage.total_positions, 3)
        self.assertTrue(StoragePosition.objects.filter(pk=protected_position.pk).exists())
        self.assertEqual(
            list(StoragePosition.objects.filter(storage=self.storage).order_by("name").values_list("name", flat=True)),
            [1, 2, 3],
        )

    def test_set_positions_can_shrink_to_value_higher_than_highest_stored_position(self):
        self.storage.set_positions(5)
        protected_position = StoragePosition.objects.get(storage=self.storage, name=3)
        SampleFactory(position=protected_position)

        self.storage.set_positions(4)

        self.assertEqual(self.storage.total_positions, 4)
        self.assertTrue(StoragePosition.objects.filter(pk=protected_position.pk).exists())
        self.assertEqual(
            list(StoragePosition.objects.filter(storage=self.storage).order_by("name").values_list("name", flat=True)),
            [1, 2, 3, 4],
        )

    def test_set_positions_cannot_shrink_below_highest_stored_position(self):
        self.storage.set_positions(5)
        protected_position = StoragePosition.objects.get(storage=self.storage, name=3)
        SampleFactory(position=protected_position)

        with self.assertRaises(ValueError):
            self.storage.set_positions(2)

        self.assertTrue(StoragePosition.objects.filter(pk=protected_position.pk).exists())
        self.assertEqual(self.storage.total_positions, 5)
        self.assertEqual(
            list(StoragePosition.objects.filter(storage=self.storage).order_by("name").values_list("name", flat=True)),
            [1, 2, 3, 4, 5],
        )

    def test_set_positions_uses_highest_stored_position_not_stored_positions_count(self):
        self.storage.set_positions(10)
        positions = StoragePosition.objects.filter(storage=self.storage, name__in=(1, 3, 5)).order_by("name")
        for position in positions:
            SampleFactory(position=position)

        with self.assertRaises(ValueError):
            self.storage.set_positions(3)

        self.assertEqual(self.storage.total_positions, 10)
        self.assertTrue(StoragePosition.objects.filter(pk=positions[0].pk).exists())
        self.assertTrue(StoragePosition.objects.filter(pk=positions[1].pk).exists())
        self.assertTrue(StoragePosition.objects.filter(pk=positions[2].pk).exists())

    def test_set_positions_preserves_empty_holes_when_shrinking_to_highest_stored_position(self):
        self.storage.set_positions(10)
        positions = StoragePosition.objects.filter(storage=self.storage, name__in=(1, 3, 5)).order_by("name")
        for position in positions:
            SampleFactory(position=position)

        self.storage.set_positions(5)

        self.assertEqual(self.storage.total_positions, 5)
        self.assertEqual(
            list(StoragePosition.objects.filter(storage=self.storage).order_by("name").values_list("name", flat=True)),
            [1, 2, 3, 4, 5],
        )
        self.assertTrue(StoragePosition.objects.filter(pk=positions[0].pk).exists())
        self.assertTrue(StoragePosition.objects.filter(pk=positions[1].pk).exists())
        self.assertTrue(StoragePosition.objects.filter(pk=positions[2].pk).exists())

    def test_storage_position_with_associated_sample_cannot_be_deleted_directly(self):
        self.storage.set_positions(1)
        position = StoragePosition.objects.get(storage=self.storage, name=1)
        SampleFactory(position=position)

        with self.assertRaises(ProtectedError):
            position.delete()

        self.assertTrue(StoragePosition.objects.filter(pk=position.pk).exists())
