from factory.declarations import Sequence, SubFactory
from factory.django import DjangoModelFactory

from collect.models import Cart, CartItem, Sample, SampleWeight, Storage, StoragePosition
from frontpage.factories import UserFactory
from register.factories import PlantVarietyFactory


class StorageFactory(DjangoModelFactory):
    class Meta:
        model = Storage

    name = Sequence(lambda n: f"B{n}")
    order = Sequence(lambda n: n)


class StoragePositionFactory(DjangoModelFactory):
    class Meta:
        model = StoragePosition

    name = Sequence(lambda n: n)
    storage = SubFactory(StorageFactory)


class SampleFactory(DjangoModelFactory):
    class Meta:
        model = Sample

    sample_id = Sequence(lambda n: n)
    variety = SubFactory(PlantVarietyFactory)
    notes = "Test note"
    growing_season = 2025
    position = SubFactory(StoragePositionFactory)


class SampleWeightFactory(DjangoModelFactory):
    class Meta:
        model = SampleWeight

    sample = SubFactory(SampleFactory)
    weight = 20


class CartFactory(DjangoModelFactory):
    class Meta:
        model = Cart

    name = "TestCart"
    user = SubFactory(UserFactory)
    is_active = True


class CartItemFactory(DjangoModelFactory):
    class Meta:
        model = CartItem

    sample = SubFactory(SampleFactory)
    weight = 10
    cart = SubFactory(CartFactory)
    order = Sequence(lambda n: n)
