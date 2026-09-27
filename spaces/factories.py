from factory import Faker
from factory.django import DjangoModelFactory

from spaces.models import Location


class LocationFactory(DjangoModelFactory):
    name = Faker("city")
    longitude = Faker("longitude")
    latitude = Faker("latitude")

    class Meta:
        model = Location
