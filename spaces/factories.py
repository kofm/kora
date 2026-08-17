from factory import Faker, Sequence
from factory.django import DjangoModelFactory

from spaces.models import Location


class LocationFactory(DjangoModelFactory):
    name = Faker("city")
    order = Sequence(lambda n: n)
    longitude = Faker("longitude")
    latitude = Faker("latitude")

    class Meta:
        model = Location
