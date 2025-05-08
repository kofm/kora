from django.core.exceptions import ValidationError
from django.test import TestCase

from collect.factories import CartItemFactory, SampleFactory, SampleWeightFactory


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
