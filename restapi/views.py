"""
Kora API
"""

from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from collect.models import CartItem, SampleWeight, SeedSample, Storage, StoragePosition
from collect.serializers import SampleWeightSerializer
from describe.models import (
    Description,
    Expression,
    Protocol,
    State,
    Trait,
    Workspace,
    WorkspaceElement,
)
from parameters.models import VarietalParameter
from register.models import Entity, PlantSpecies, PlantVariety, Protection
from restapi.serializers import (
    CartSerializer,
    DescriptionSerializer,
    EntitySerializer,
    ExpressionSerializer,
    PlantSpeciesSerializer,
    PlantVarietySerializer,
    ProtectionSerializer,
    ProtocolSerializer,
    SeedSampleSerializer,
    StateSerializer,
    StoragePositionSerializer,
    StorageSerializer,
    TraitSerializer,
    VarietalParameterSerializer,
    WorkspaceElementSerializer,
    WorkspaceSerializer,
)

from .filters import (
    DescriptionFilter,
    EntityFilter,
    PlantSpeciesFilter,
    PlantVarietyFilter,
    ProtectionFilter,
    ProtocolFilter,
    SampleWeightFilter,
    SeedSampleFilter,
    StorageFilter,
    StoragePositionFilter,
)


class PlantSpeciesViewSet(viewsets.ModelViewSet):
    """
    API endpoint to view/edit a Crop
    """

    queryset = PlantSpecies.objects.all()
    serializer_class = PlantSpeciesSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = PlantSpeciesFilter


class PlantVarietyViewSet(viewsets.ModelViewSet):
    queryset = PlantVariety.objects.all()
    serializer_class = PlantVarietySerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = PlantVarietyFilter


class EntityViewSet(viewsets.ModelViewSet):
    queryset = Entity.objects.all()
    serializer_class = EntitySerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = EntityFilter


class ProtectionViewSet(viewsets.ModelViewSet):
    queryset = Protection.objects.all()
    serializer_class = ProtectionSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = ProtectionFilter


class ProtocolViewSet(viewsets.ModelViewSet):
    queryset = Protocol.objects.all()
    serializer_class = ProtocolSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = ProtocolFilter


class StateViewSet(viewsets.ModelViewSet):
    queryset = State.objects.all()
    serializer_class = StateSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["trait"]


class TraitViewSet(viewsets.ModelViewSet):
    queryset = Trait.objects.all()
    serializer_class = TraitSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["protocol"]


class DescriptionViewSet(viewsets.ModelViewSet):
    serializer_class = DescriptionSerializer
    queryset = Description.objects.all()
    filter_backends = [DjangoFilterBackend]
    filterset_class = DescriptionFilter


class ExpressionViewSet(viewsets.ModelViewSet):
    serializer_class = ExpressionSerializer
    queryset = Expression.objects.all()


class VarietalParameterViewSet(viewsets.ModelViewSet):
    queryset = VarietalParameter.objects.all()
    serializer_class = VarietalParameterSerializer


class StorageViewSet(viewsets.ModelViewSet):
    queryset = Storage.objects.all()
    serializer_class = StorageSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = StorageFilter


class StoragePositionViewSet(viewsets.ModelViewSet):
    queryset = StoragePosition.objects.all()
    serializer_class = StoragePositionSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = StoragePositionFilter


class SeedSampleViewSet(viewsets.ModelViewSet):
    queryset = SeedSample.objects.all()
    serializer_class = SeedSampleSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = SeedSampleFilter


class SampleWeightViewSet(viewsets.ModelViewSet):
    queryset = SampleWeight.objects.all()
    serializer_class = SampleWeightSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = SampleWeightFilter


class CartItemViewSet(viewsets.ModelViewSet):
    serializer_class = CartSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        cart = self.kwargs["cart"]
        # FIXME: weight retrieval is inefficient!
        return CartItem.objects.select_related("sample__variety", "sample__position").filter(
            cart__user=user, cart__pk=cart
        )


class WorkspaceViewSet(viewsets.ModelViewSet):
    serializer_class = WorkspaceSerializer

    def get_queryset(self):
        user = self.request.user
        return Workspace.objects.filter(user=user)


class WorkspaceElementViewSet(viewsets.ModelViewSet):
    serializer_class = WorkspaceElementSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        workspace = self.kwargs["list"]
        return WorkspaceElement.objects.filter(workspace__user=user, workspace__pk=workspace)
