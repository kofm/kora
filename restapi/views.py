from .filters import DescriptionFilter
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from describe.models import Description, Protocol, Expression, State, Trait
from parameters.models import VarietalParameter
from collect.models import CartItem, SeedSample, StoragePosition

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
    StateSerializer,
    TraitSerializer,
    SeedSampleSerializer,
    StoragePositionSerializer,
    VarietalParameterSerializer,
)


class PlantSpeciesViewSet(viewsets.ModelViewSet):
    """
    API endpoint to view/edit a Crop
    """

    queryset = PlantSpecies.objects.all()
    serializer_class = PlantSpeciesSerializer


class PlantVarietyViewSet(viewsets.ModelViewSet):
    queryset = PlantVariety.objects.all()
    serializer_class = PlantVarietySerializer

    def get_queryset(self):
        species = self.request.query_params.get("species", None)
        queryset = PlantVariety.objects.all()
        if species is not None:
            queryset = queryset.filter(species=species)
        return queryset


class EntityViewSet(viewsets.ModelViewSet):
    queryset = Entity.objects.all()
    serializer_class = EntitySerializer


class ProtectionViewSet(viewsets.ModelViewSet):
    queryset = Protection.objects.all()
    serializer_class = ProtectionSerializer


class ProtocolViewSet(viewsets.ModelViewSet):
    queryset = Protocol.objects.all()
    serializer_class = ProtocolSerializer


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


class SeedSampleViewSet(viewsets.ModelViewSet):
    queryset = SeedSample.objects.all()
    serializer_class = SeedSampleSerializer


class CartItemViewSet(viewsets.ModelViewSet):
    serializer_class = CartSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        cart = self.kwargs["cart"]
        return CartItem.objects.filter(cart__user=user, cart__pk=cart)


class StoragePositionViewSet(viewsets.ModelViewSet):
    queryset = StoragePosition.objects.all()
    serializer_class = StoragePositionSerializer
