import datetime

from factory import faker
from factory.declarations import Iterator, LazyFunction, SubFactory
from factory.django import DjangoModelFactory

from register.models import Entity, PlantSpecies, PlantVariety, PlantVarietyName, Protection

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

    common_name = Iterator([species[0] for species in PLANT_SPECIES])
    latin_name = Iterator([species[1] for species in PLANT_SPECIES])
    plant_type = Iterator([species[2] for species in PLANT_SPECIES])


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


class ProtectionFactory(DjangoModelFactory):
    class Meta:
        model = Protection

    type = "NLI"
    status = "G"
    country = "IT"
    variety = SubFactory(PlantVarietyFactory)
