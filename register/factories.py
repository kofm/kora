import datetime

from factory import faker
from factory.declarations import Iterator, LazyFunction, Sequence, SubFactory
from factory.django import DjangoModelFactory

from register.models import Entity, PlantSpecies, PlantVariety, PlantVarietyName

PLANT_SPECIES = [
    ("Tomato", "Solanum lycopersicum", "vegetable"),
    ("Wheat", "Triticum aestivum", "herbaceous"),
    ("Olive", "Olea europaea", "tree"),
    ("Rose", "Rosa spp.", "shrub"),
    ("Mint", "Mentha spicata", "herbaceous"),
    ("Maize", "Zea mays", "vegetable"),
    ("Pea", "Pisum sativum", "herbaceous"),
]


class PlantSpeciesFactory(DjangoModelFactory):
    class Meta:
        model = PlantSpecies

    common_name = Sequence(lambda n: f"Species Common Name {n}")
    latin_name = Sequence(lambda n: f"Species Latin Name {n}")
    plant_type = Iterator(["vegetable", "tree", "shrub", "herbaceous"])


class PlantVarietyFactory(DjangoModelFactory):
    class Meta:
        model = PlantVariety

    name = "Cherry Tomato"
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
