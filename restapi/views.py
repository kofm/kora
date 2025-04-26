"""
Kora API
"""

from django.db.models.query import Prefetch
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status, viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from collect.models import Cart, CartItem, Sample, SampleWeight, Storage, StoragePosition
from collect.serializers import SampleWeightSerializer
from describe.models import (
    Description,
    Protocol,
    Trait,
    Workspace,
    WorkspaceElement,
)
from parameters.models import Parameter, VarietalParameter
from register.models import Entity, PlantSpecies, PlantVariety, Protection
from restapi.serializers import (
    CartItemSerializer,
    DescriptionSerializer,
    EntitySerializer,
    ParameterSerializer,
    PlantSpeciesSerializer,
    PlantVarietySerializer,
    ProtectionSerializer,
    ProtocolSerializer,
    SampleSerializer,
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
    StorageFilter,
    StoragePositionFilter,
    TraitFilter,
    VarietalParameterFilter,
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
    queryset = PlantVariety.objects.all().prefetch_related("names").order_by("created_at")
    serializer_class = PlantVarietySerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = PlantVarietyFilter
    permission_classes = [IsAuthenticated]


class EntityViewSet(viewsets.ModelViewSet):
    queryset = Entity.objects.all()
    serializer_class = EntitySerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = EntityFilter


class ProtectionViewSet(viewsets.ModelViewSet):
    serializer_class = ProtectionSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = ProtectionFilter

    def get_queryset(self):
        entity_qs = Entity.objects.all().order_by("name")
        return (
            Protection.objects.select_related("variety__species")
            .prefetch_related(Prefetch("applicants", queryset=entity_qs), Prefetch("maintainers", queryset=entity_qs))
            .select_related("variety__species")
        )


class ProtocolViewSet(viewsets.ModelViewSet):
    queryset = Protocol.objects.select_related("plantspecies").all()
    serializer_class = ProtocolSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = ProtocolFilter


class TraitViewSet(viewsets.ModelViewSet):
    queryset = Trait.objects.select_related("protocol").prefetch_related("states").all()
    serializer_class = TraitSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = TraitFilter


class DescriptionViewSet(viewsets.ModelViewSet):
    serializer_class = DescriptionSerializer
    queryset = (
        Description.objects.select_related("variety__species", "protocol")
        .prefetch_related("expressions__state__trait")
        .all()
    )
    filter_backends = [DjangoFilterBackend]
    filterset_class = DescriptionFilter


class ParameterViewSet(viewsets.ModelViewSet):
    queryset = Parameter.objects.all()
    serializer_class = ParameterSerializer


class VarietalParameterViewSet(viewsets.ModelViewSet):
    queryset = VarietalParameter.objects.select_related("parameter").all()
    serializer_class = VarietalParameterSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = VarietalParameterFilter


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


class SampleViewSet(viewsets.ModelViewSet):
    queryset = Sample.objects.with_availability().with_germination()
    serializer_class = SampleSerializer


class SampleWeightViewSet(viewsets.ModelViewSet):
    queryset = SampleWeight.objects.select_related("sample").all()
    serializer_class = SampleWeightSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = SampleWeightFilter


class CartItemViewSet(viewsets.ModelViewSet):
    serializer_class = CartItemSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        cart = self.kwargs["cart"]
        return CartItem.objects.select_related("sample__variety__species", "sample__position__storage").filter(
            cart__user=user, cart__pk=cart
        )

    def create(self, request, *args, **kwargs):
        user = request.user
        cart_id = self.kwargs["cart"]
        try:
            cart = Cart.objects.get(pk=cart_id, user=user)
        except Cart.DoesNotExist:
            return Response({"detail": "Cart not found."}, status=status.HTTP_404_NOT_FOUND)
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(cart=cart)  # Associate the cart with the new CartItem
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


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
        workspace = self.kwargs["workspace"]
        return (
            WorkspaceElement.objects.select_related("description__variety__species", "description__protocol")
            .prefetch_related("description__expressions__state__trait")
            .filter(workspace__user=user, workspace__pk=workspace)
        )
