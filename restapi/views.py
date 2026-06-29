"""
Kora API
"""

from django.db import transaction
from django.db.models.query import Prefetch
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.serializers import ValidationError

from collect.models import Cart, CartItem, Germinability, Sample, SampleWeight, Storage, StoragePosition
from collect.serializers import GerminabilitySerializer, SampleWeightSerializer
from describe.models import (
    Description,
    Expression,
    Protocol,
    State,
    Trait,
    Workspace,
    WorkspaceElement,
)
from parameters.models import Parameter, VarietalParameter
from register.models import Entity, PlantSpecies, PlantVariety, PlantVarietyName, Protection
from register.serializers import EntityImportSerializer, PlantVarietyImportSerializer, ProtectionExcelImportSerializer
from restapi.serializers.models import (
    CartItemSerializer,
    CartSerializer,
    DescriptionSerializer,
    EntitySerializer,
    ExpressionSerializer,
    ParameterSerializer,
    PlantSpeciesSerializer,
    PlantVarietySerializer,
    ProtectionSerializer,
    ProtocolSerializer,
    SampleSerializer,
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
    ExpressionFilter,
    GerminabilityFilter,
    ParameterFilter,
    PlantSpeciesFilter,
    PlantVarietyFilter,
    ProtectionFilter,
    ProtocolFilter,
    SampleFilter,
    SampleWeightFilter,
    StateFilter,
    StorageFilter,
    StoragePositionFilter,
    TraitFilter,
    VarietalParameterFilter,
)


class BulkCreateMixin:
    @transaction.atomic
    def create(self, request, *args, **kwargs):
        is_many = isinstance(request.data, list)
        serializer = self.get_serializer(data=request.data, many=is_many)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class PlantSpeciesViewSet(BulkCreateMixin, viewsets.ModelViewSet):
    queryset = PlantSpecies.objects.all()
    serializer_class = PlantSpeciesSerializer
    filterset_class = PlantSpeciesFilter


class PlantVarietyViewSet(BulkCreateMixin, viewsets.ModelViewSet):
    queryset = PlantVariety.objects.all().select_related("species").prefetch_related("names").order_by("created_at")
    serializer_class = PlantVarietySerializer
    filterset_class = PlantVarietyFilter

    @action(
        detail=False,
        methods=["post"],
        serializer_class=PlantVarietyImportSerializer,
    )
    def excel_import(self, request):
        """Import varieties from an Excel table.

        Only the name of the variety and the species it belongs are required.
        The columns should be named as following, in lower case:

        - `name`: the name of the variety;
        - `species`: the PRIMARY KEY of the species;

        NOTE: if a variety of the same species with the same name
          already exists, it will not be imported. If you really need
          a variety with the same name you will have to add it through
          the user interface.
        """
        serializer = PlantVarietyImportSerializer(data=request.data)

        if not serializer.is_valid():
            return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)

        try:
            objs = serializer.save()
        except ValidationError as exc:
            errors = serializer.catch_row_serializer_errors(exc)
            return Response(errors, status.HTTP_400_BAD_REQUEST)

        if not objs:
            return Response({"success": "all rows valid"}, status.HTTP_202_ACCEPTED)

        with transaction.atomic():
            created = PlantVariety.objects.bulk_create([obj for obj in objs if obj], batch_size=1000)
            PlantVarietyName.objects.bulk_create(
                [PlantVarietyName(name=obj.name, variety=obj) for obj in created],
                batch_size=1000,
            )

        varieties = (
            PlantVariety.objects.select_related("species")
            .prefetch_related("names")
            .filter(pk__in=[obj.pk for obj in created])[:100]
        )
        out_ser = PlantVarietySerializer(varieties, many=True)

        return Response(out_ser.data, status.HTTP_201_CREATED)


class EntityViewSet(BulkCreateMixin, viewsets.ModelViewSet):
    queryset = Entity.objects.all()
    serializer_class = EntitySerializer
    filterset_class = EntityFilter

    @action(detail=False, methods=["post"], serializer_class=EntityImportSerializer)
    def excel_import(self, request):
        ser = EntityImportSerializer(data=request.data)

        if not ser.is_valid():
            return Response(ser.errors, status.HTTP_400_BAD_REQUEST)

        try:
            objs = ser.save()
        except ValidationError as exc:
            errors = ser.catch_row_serializer_errors(exc)
            return Response(errors, status.HTTP_400_BAD_REQUEST)

        if not objs:
            return Response({"success": "all rows are valid"}, status.HTTP_202_ACCEPTED)

        created = Entity.objects.bulk_create([obj for obj in objs if obj], batch_size=1000)
        out = EntitySerializer(created, many=True)
        return Response(out.data, status.HTTP_201_CREATED)


class ProtectionViewSet(BulkCreateMixin, viewsets.ModelViewSet):
    serializer_class = ProtectionSerializer
    filterset_class = ProtectionFilter

    def get_queryset(self):
        entity_qs = Entity.objects.all().order_by("name")
        return Protection.objects.select_related("type").prefetch_related(
            Prefetch("applicants", queryset=entity_qs), Prefetch("maintainers", queryset=entity_qs)
        )

    @action(
        detail=False,
        methods=["post"],
        serializer_class=ProtectionExcelImportSerializer,
    )
    def excel_import(self, request):
        sr = ProtectionExcelImportSerializer(data=request.data)
        if not sr.is_valid():
            return Response(sr.errors, status=status.HTTP_400_BAD_REQUEST)

        try:
            objs = sr.save()
        except ValidationError as exc:
            errors = sr.catch_row_serializer_errors(exc)
            return Response(errors, status=status.HTTP_400_BAD_REQUEST)

        if not objs:
            return Response({"success": "all rows are valid"}, status.HTTP_202_ACCEPTED)

        with transaction.atomic():
            Protection.objects.bulk_create([obj for obj, apps, mains in objs if obj])

            apps_through = Protection.applicants.through
            mains_through = Protection.maintainers.through
            apps_rels = []
            mains_rels = []
            for prot, apps, mains in objs:
                for entity in apps:
                    apps_rels.append(apps_through(protection_id=prot.id, entity_id=entity.id))
                for entity in mains:
                    mains_rels.append(mains_through(protection_id=prot.id, entity_id=entity.id))
            apps_through.objects.bulk_create(apps_rels, batch_size=1000)
            mains_through.objects.bulk_create(mains_rels, batch_size=1000)

        ids = [obj.id for obj, _, _ in objs if obj]
        protections = (
            Protection.objects.filter(id__in=ids)
            .select_related("variety")
            .prefetch_related("applicants", "maintainers")
        )
        out = ProtectionSerializer(protections, many=True)
        return Response(out.data, status=status.HTTP_201_CREATED)


class ProtocolViewSet(BulkCreateMixin, viewsets.ModelViewSet):
    queryset = Protocol.objects.select_related("plantspecies").all()
    serializer_class = ProtocolSerializer
    filterset_class = ProtocolFilter


class TraitViewSet(BulkCreateMixin, viewsets.ModelViewSet):
    queryset = Trait.objects.all()
    serializer_class = TraitSerializer
    filterset_class = TraitFilter


class StateViewSet(BulkCreateMixin, viewsets.ModelViewSet):
    queryset = State.objects.select_related("trait").all()
    serializer_class = StateSerializer
    filterset_class = StateFilter


class DescriptionViewSet(BulkCreateMixin, viewsets.ModelViewSet):
    serializer_class = DescriptionSerializer
    queryset = Description.objects.select_related("variety__species", "protocol", "label").all()
    filterset_class = DescriptionFilter


class ExpressionViewSet(BulkCreateMixin, viewsets.ModelViewSet):
    serializer_class = ExpressionSerializer
    queryset = Expression.objects.select_related("description", "state__trait").all()
    filterset_class = ExpressionFilter


class ParameterViewSet(BulkCreateMixin, viewsets.ModelViewSet):
    queryset = Parameter.objects.all()
    serializer_class = ParameterSerializer
    filterset_class = ParameterFilter


class VarietalParameterViewSet(BulkCreateMixin, viewsets.ModelViewSet):
    queryset = VarietalParameter.objects.select_related("parameter").all()
    serializer_class = VarietalParameterSerializer
    filterset_class = VarietalParameterFilter


class StorageViewSet(BulkCreateMixin, viewsets.ModelViewSet):
    queryset = Storage.objects.all()
    serializer_class = StorageSerializer
    filterset_class = StorageFilter


class StoragePositionViewSet(BulkCreateMixin, viewsets.ModelViewSet):
    queryset = StoragePosition.objects.all()
    serializer_class = StoragePositionSerializer
    filterset_class = StoragePositionFilter


class SampleViewSet(BulkCreateMixin, viewsets.ModelViewSet):
    queryset = Sample.objects.with_availability().with_germination()
    serializer_class = SampleSerializer
    filterset_class = SampleFilter


class SampleWeightViewSet(BulkCreateMixin, viewsets.ModelViewSet):
    queryset = SampleWeight.objects.select_related("sample").all()
    serializer_class = SampleWeightSerializer
    filterset_class = SampleWeightFilter


class GerminabilityViewSet(BulkCreateMixin, viewsets.ModelViewSet):
    queryset = Germinability.objects.select_related("sample").all()
    serializer_class = GerminabilitySerializer
    filterset_class = GerminabilityFilter


class CartItemViewSet(viewsets.ModelViewSet):
    serializer_class = CartItemSerializer

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
        many = isinstance(request.data, list)
        serializer = self.get_serializer(data=request.data, many=many)
        serializer.is_valid(raise_exception=True)
        serializer.save(cart=cart)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


class CartViewSet(viewsets.ModelViewSet):
    serializer_class = CartSerializer

    def get_queryset(self):
        user = self.request.user
        return Cart.objects.filter(user=user)


class WorkspaceViewSet(viewsets.ModelViewSet):
    serializer_class = WorkspaceSerializer

    def get_queryset(self):
        user = self.request.user
        return Workspace.objects.filter(user=user)


class WorkspaceElementViewSet(viewsets.ModelViewSet):
    serializer_class = WorkspaceElementSerializer

    def get_queryset(self):
        user = self.request.user
        workspace = self.kwargs["workspace"]
        return (
            WorkspaceElement.objects.select_related(
                "description__variety__species",
                "description__protocol",
                "description__label",
            )
            .prefetch_related("description__expressions__state__trait")
            .filter(workspace__user=user, workspace__pk=workspace)
        )

    def create(self, request, *args, **kwargs):
        user = request.user
        workspace_id = self.kwargs["workspace"]
        try:
            workspace = Workspace.objects.get(pk=workspace_id, user=user)
        except Workspace.DoesNotExist:
            return Response({"detail": "Workspace not found."}, status=status.HTTP_404_NOT_FOUND)

        many = isinstance(request.data, list)
        serializer = self.get_serializer(data=request.data, many=many)
        serializer.is_valid(raise_exception=True)
        serializer.save(workspace=workspace)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
