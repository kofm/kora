from factory import Faker, SelfAttribute, Sequence, SubFactory
from factory.django import DjangoModelFactory

from calculator.models import Crop, CropLayout, FieldBook, ParameterObservation, Step
from register.factories import PlantVarietyFactory
from spaces.factories import LocationFactory


class CropLayoutFactory(DjangoModelFactory):
    name = Sequence(lambda n: f"Layout {n}")
    location = SubFactory(LocationFactory)
    ncol = 4

    class Meta:
        model = CropLayout


class CropFactory(DjangoModelFactory):
    variety = SubFactory(PlantVarietyFactory)
    layout = SubFactory(CropLayoutFactory)
    order = Sequence(lambda n: n)

    class Meta:
        model = Crop


class FieldBookFactory(DjangoModelFactory):
    name = Faker("word")
    layout = SubFactory(CropLayoutFactory)

    class Meta:
        model = FieldBook


class StepFactory(DjangoModelFactory):
    fieldbook = SubFactory(FieldBookFactory)
    crop = SubFactory(CropFactory, layout=SelfAttribute("..fieldbook.layout"))
    order = Sequence(lambda n: n)

    class Meta:
        model = Step


class ParameterObservationFactory(DjangoModelFactory):
    crop = SubFactory(CropFactory)
    parameter = SubFactory("parameters.factories.ParameterFactory")
    parameter_value = 1
    created_by = SubFactory("frontpage.factories.UserFactory")

    class Meta:
        model = ParameterObservation
