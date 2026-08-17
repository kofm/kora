from factory import faker
from factory.django import DjangoModelFactory

from parameters.models import Parameter


class ParameterFactory(DjangoModelFactory):
    code = faker.Faker("word")
    name = faker.Faker("word")
    description = faker.Faker("sentence")
    measure_unit = faker.Faker("random_lowercase_letter")

    class Meta:
        model = Parameter
