from factory.declarations import Sequence, SubFactory
from factory.django import DjangoModelFactory

from describe.models import Description, Expression, Protocol, State, Trait, Workspace, WorkspaceElement
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

    numeric_id = Sequence(lambda n: n)
    description = "Leaf: colour"
    protocol = SubFactory(ProtocolFactory)


class StateFactory(DjangoModelFactory):
    class Meta:
        model = State

    numeric_id = Sequence(lambda n: n)
    trait = SubFactory(TraitFactory)
    description = "light"


class DescriptionFactory(DjangoModelFactory):
    class Meta:
        model = Description

    name = "Official"
    variety = SubFactory(PlantVarietyFactory)
    protocol = SubFactory(ProtocolFactory)


class ExpressionFactory(DjangoModelFactory):
    class Meta:
        model = Expression

    description = SubFactory(DescriptionFactory)
    state = SubFactory(StateFactory)
    note = "My Expression Note"


class WorkspaceFactory(DjangoModelFactory):
    class Meta:
        model = Workspace

    name = "A workspace"
    is_active = True


class WorkspaceElementFactory(DjangoModelFactory):
    class Meta:
        model = WorkspaceElement

    description = SubFactory(DescriptionFactory)
    order = Sequence(lambda n: n)
