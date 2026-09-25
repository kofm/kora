import datetime

from factory import faker
from factory.declarations import Iterator, LazyFunction, SubFactory
from factory.django import DjangoModelFactory
from factory.fuzzy import FuzzyText

from register.models import Entity, PlantSpecies, PlantVariety, PlantVarietyName, Protection, ProtectionType

PLANT_SPECIES = [
    ("Tomato", "Solanum lycopersicum"),
    ("Wheat", "Triticum aestivum"),
    ("Olive", "Olea europaea"),
    ("Rose", "Rosa spp."),
    ("Mint", "Mentha spicata"),
    ("Maize", "Zea mays"),
    ("Pea", "Pisum sativum"),
]


class PlantSpeciesFactory(DjangoModelFactory):
    class Meta:
        model = PlantSpecies
        django_get_or_create = ("common_name",)

    common_name = Iterator([species[0] for species in PLANT_SPECIES])
    botanical_name = Iterator([species[1] for species in PLANT_SPECIES])


class PlantVarietyFactory(DjangoModelFactory):
    class Meta:
        model = PlantVariety

    name = faker.Faker("first_name")
    species = SubFactory(PlantSpeciesFactory)


class PlantVarietyNameFactory(DjangoModelFactory):
    class Meta:
        model = PlantVarietyName

    name = faker.Faker("first_name")
    variety = SubFactory(PlantVarietyFactory)
    change_date = LazyFunction(datetime.datetime.now)


class EntityFactory(DjangoModelFactory):
    class Meta:
        model = Entity

    name = "SeedCo"
    type = "CO"
    country = "US"
    contact = "123 Seed St"
    email = "contact@seedco.com"


class ProtectionTypeFactory(DjangoModelFactory):
    code = FuzzyText(length=3)
    name = faker.Faker("word")

    class Meta:
        model = ProtectionType


class NationalListingFactory(DjangoModelFactory):
    code = "NLI"
    name = "National Listing"

    class Meta:
        model = ProtectionType
        django_get_or_create = ("code",)


class ProtectionFactory(DjangoModelFactory):
    type = SubFactory(NationalListingFactory)
    status = "G"
    country = "IT"
    variety = SubFactory(PlantVarietyFactory)

    class Meta:
        model = Protection
