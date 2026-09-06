from factory import Faker, LazyAttribute, SelfAttribute, Sequence, SubFactory
from factory.django import DjangoModelFactory

from calculator.models import (
    Crop,
    CropLayout,
    FieldBook,
    Management,
    ManagementType,
    ParameterObservation,
    Step,
    TraitObservation,
)
from describe.factories import StateFactory
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


class ManagementTypeFactory(DjangoModelFactory):
    code = Sequence(lambda number: f"management-{number}")
    name = Sequence(lambda number: f"Management {number}")

    class Meta:
        model = ManagementType


class ManagementFactory(DjangoModelFactory):
    type = SubFactory(ManagementTypeFactory)
    layout = SubFactory(CropLayoutFactory)
    date = Faker("date_object")

    class Meta:
        model = Management


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


class TraitObservationFactory(DjangoModelFactory):
    crop = SubFactory(CropFactory)
    state = LazyAttribute(
        lambda observation: StateFactory(trait__protocol__plantspecies=observation.crop.variety.species)
    )
    created_by = SubFactory("frontpage.factories.UserFactory")

    class Meta:
        model = TraitObservation
