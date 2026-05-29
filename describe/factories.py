from factory.declarations import Sequence, SubFactory
from factory.django import DjangoModelFactory
from factory.faker import Faker

from describe.models import (
    Description,
    DescriptionLabel,
    Expression,
    Protocol,
    State,
    StateGroup,
    Trait,
    Workspace,
    WorkspaceElement,
)
from register.factories import PlantSpeciesFactory, PlantVarietyFactory


class ProtocolFactory(DjangoModelFactory):
    class Meta:
        model = Protocol

    name = "TP123"
    plantspecies = SubFactory(PlantSpeciesFactory)
    order = Sequence(lambda n: n)


class TraitFactory(DjangoModelFactory):
    class Meta:
        model = Trait

    numeric_id = Sequence(lambda n: n + 1)
    description = "Leaf: colour"
    protocol = SubFactory(ProtocolFactory)


class StateGroupFactory(DjangoModelFactory):
    class Meta:
        model = StateGroup


class StateFactory(DjangoModelFactory):
    numeric_id = Sequence(lambda n: n + 1)
    trait = SubFactory(TraitFactory)
    description = Faker("word", part_of_speech="adjective")
    group = SubFactory(StateGroupFactory)

    class Meta:
        model = State


class DescriptionLabelFactory(DjangoModelFactory):
    name = Faker("word", part_of_speech="adjective")

    class Meta:
        model = DescriptionLabel


class DescriptionFactory(DjangoModelFactory):
    label = SubFactory(DescriptionLabelFactory)
    variety = SubFactory(PlantVarietyFactory)
    protocol = SubFactory(ProtocolFactory)

    class Meta:
        model = Description


class ExpressionFactory(DjangoModelFactory):
    description = SubFactory(DescriptionFactory)
    state = SubFactory(StateFactory)
    note = "My Expression Note"

    class Meta:
        model = Expression


class WorkspaceFactory(DjangoModelFactory):
    name = "A workspace"
    is_active = True

    class Meta:
        model = Workspace


class WorkspaceElementFactory(DjangoModelFactory):
    description = SubFactory(DescriptionFactory)
    order = Sequence(lambda n: n)

    class Meta:
        model = WorkspaceElement
