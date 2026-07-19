"""Kora API"""

from django.db import transaction
from django.db.models.query import Prefetch
from drf_spectacular.utils import extend_schema
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.generics import get_object_or_404

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
from register.models import Entity, PlantSpecies, PlantVariety, PlantVarietyName, Protection, ProtectionType
from register.serializers import (
    EntityImportRequestSerializer,
    PlantVarietyImportRequestSerializer,
    ProtectionImportRequestSerializer,
)
from restapi.decorators import document_bulk_create
from restapi.serializers.generic import ExcelImportResponseSerializer
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
    ProtectionTypeSerializer,
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
from restapi.viewsets import ExcelImportActionMixin, KoraViewSet

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


@document_bulk_create(PlantSpeciesSerializer, name="plant species")
class PlantSpeciesViewSet(KoraViewSet):
    queryset = PlantSpecies.objects.all()
    serializer_class = PlantSpeciesSerializer
    filterset_class = PlantSpeciesFilter


@document_bulk_create(PlantVarietySerializer, name="plant varieties")
class PlantVarietyViewSet(ExcelImportActionMixin, KoraViewSet):
    queryset = PlantVariety.objects.all().select_related("species").prefetch_related("names").order_by("created_at")
    serializer_class = PlantVarietySerializer
    filterset_class = PlantVarietyFilter

    def perform_excel_import_create(self, objs):
        with transaction.atomic():
            created = PlantVariety.objects.bulk_create(
                [obj for obj in objs if obj],
                batch_size=1000,
            )
            PlantVarietyName.objects.bulk_create(
                [PlantVarietyName(name=obj.name, variety=obj) for obj in created],
                batch_size=1000,
            )
        return len(created)

    @extend_schema(responses=ExcelImportResponseSerializer)
    @action(detail=False, methods=["post"], serializer_class=PlantVarietyImportRequestSerializer)
    def excel_import(self, request):
        """Import varieties from a spreadsheet file.

        Supported file formats are CSV, XLS, XLSX, and ODS. The first
        row must contain the column names described below.

        Select ``Validate only`` to check the file for errors without
        importing any rows.

        **Accepted columns**:

        - ``name`` (text, required): denomination of the variety;
        - ``species_id`` (integer, required): ID of the species (see
          :http:get:`/api/species/`).

        A row is skipped if a variety with the same ``name`` and
        ``species_id`` already exists. Existing varieties are not updated.
        To create another variety with the same name, use the user interface.
        """
        return super().excel_import(request)


@document_bulk_create(EntitySerializer, name="entities")
class EntityViewSet(ExcelImportActionMixin, KoraViewSet):
    queryset = Entity.objects.all()
    serializer_class = EntitySerializer
    filterset_class = EntityFilter

    def perform_excel_import_create(self, objs):
        created = Entity.objects.bulk_create([obj for obj in objs if obj], batch_size=1000)
        return len(created)

    @extend_schema(responses=ExcelImportResponseSerializer)
    @action(detail=False, methods=["post"], serializer_class=EntityImportRequestSerializer)
    def excel_import(self, request):
        """Import entities from a spreadsheet file.

        Supported file formats are CSV, XLS, XLSX, and ODS. The first
        row must contain the column names described below.

        Select ``Validate only`` to check the file for errors without
        importing any rows.

        **Accepted columns**:

        - ``name`` (text, required): entity name;
        - ``type`` (text, optional): entity type. Accepted values are ``IN``
          (Individual), ``PA`` (Partnership), ``CO`` (Company), and ``CP``
          (Cooperative);
        - ``country`` (text, optional): ISO 3166-1 alpha-2 country code;
        - ``contact`` (text, optional): contact information;
        - ``email`` (text, optional): email address.

        A row is skipped if an entity with the same ``name`` already exists.
        Existing entities are not updated. Semicolons in ``name`` are treated
        as part of a single entity name.
        """
        return super().excel_import(request)


class ProtectionTypeViewSet(viewsets.ModelViewSet):
    serializer_class = ProtectionTypeSerializer
    queryset = ProtectionType.objects.all()


@document_bulk_create(ProtectionSerializer, name="protections")
class ProtectionViewSet(ExcelImportActionMixin, KoraViewSet):
    serializer_class = ProtectionSerializer
    filterset_class = ProtectionFilter

    def get_queryset(self):
        entity_qs = Entity.objects.all().order_by("name")
        return Protection.objects.select_related("type").prefetch_related(
            Prefetch("applicants", queryset=entity_qs), Prefetch("maintainers", queryset=entity_qs)
        )

    def perform_excel_import_create(self, objs):
        valid_objs = [(obj, apps, mains) for obj, apps, mains in objs if obj]

        with transaction.atomic():
            protections = [obj for obj, _, _ in valid_objs]
            Protection.objects.bulk_create(protections, batch_size=1000)

            apps_through = Protection.applicants.through
            mains_through = Protection.maintainers.through

            apps_rels = [
                apps_through(protection_id=protection.id, entity_id=entity_id)
                for protection, applicants, _ in valid_objs
                for entity_id in {entity.pk for entity in applicants}
            ]
            mains_rels = [
                mains_through(protection_id=protection.id, entity_id=entity_id)
                for protection, _, maintainers in valid_objs
                for entity_id in {entity.pk for entity in maintainers}
            ]

            apps_through.objects.bulk_create(apps_rels, batch_size=1000)
            mains_through.objects.bulk_create(mains_rels, batch_size=1000)

        return len(protections)

    @extend_schema(responses=ExcelImportResponseSerializer)
    @action(detail=False, methods=["post"], serializer_class=ProtectionImportRequestSerializer)
    def excel_import(self, request):
        """Import protections from a spreadsheet file.

        Supported file formats are CSV, XLS, XLSX, and ODS. The first
        row must contain the column names described below.

        Select ``Validate only`` to check the file for errors without
        importing any rows.

        **Accepted columns**:

        - ``name`` (text, required): variety name. The variety is matched
        against existing varieties using both ``name`` and ``species_id``.
        Validation fails if no matching variety is found;
        - ``species_id`` (integer, required): ID of the variety's species
        (see :http:get:`/api/species/`);
        - ``type`` (text, required): three-letter protection type code
        (see :http:get:`/api/protection_types/`);
        - ``reference`` (text, optional): reference number or code, such as
        an application number;
        - ``status`` (text, optional): protection status. Accepted values are
        ``G`` (Granted), ``T`` (Terminated), ``A`` (Active Application),
        ``W`` (Withdrawn), ``R`` (Refused), and ``S`` (Surrendered);
        - ``country`` (text, optional): ISO 3166-1 alpha-2 country code;
        - ``date_start`` (date, optional): protection start date in
        ``YYYY-MM-DD`` format;
        - ``date_end`` (date, optional): protection end date in
        ``YYYY-MM-DD`` format;
        - ``applicants`` (text, optional): semicolon-separated applicant
        names;
        - ``maintainers`` (text, optional): semicolon-separated maintainer
        names;
        - ``note`` (text, optional): additional information.

        The ``applicants`` and ``maintainers`` columns may contain multiple
        entity names separated by semicolons, for example
        ``Entity A; Entity B``. Do not use semicolon-separated names when
        importing entities: they will be interpreted as one entity name.

        Rows whose combination of ``type``, ``name``, ``species_id``, and
        ``country`` already exists are skipped and are not updated.

        """
        return super().excel_import(request)


@document_bulk_create(ProtocolSerializer, name="protocols")
class ProtocolViewSet(KoraViewSet):
    queryset = Protocol.objects.select_related("plantspecies").all()
    serializer_class = ProtocolSerializer
    filterset_class = ProtocolFilter


@document_bulk_create(TraitSerializer, name="traits")
class TraitViewSet(KoraViewSet):
    queryset = Trait.objects.all()
    serializer_class = TraitSerializer
    filterset_class = TraitFilter


@document_bulk_create(StateSerializer, name="states")
class StateViewSet(KoraViewSet):
    queryset = State.objects.select_related("trait").all()
    serializer_class = StateSerializer
    filterset_class = StateFilter


@document_bulk_create(DescriptionSerializer, name="descriptions")
class DescriptionViewSet(KoraViewSet):
    serializer_class = DescriptionSerializer
    queryset = Description.objects.select_related("variety__species", "protocol", "label").all()
    filterset_class = DescriptionFilter


@document_bulk_create(ExpressionSerializer, name="expressions")
class ExpressionViewSet(KoraViewSet):
    serializer_class = ExpressionSerializer
    queryset = Expression.objects.select_related("description", "state__trait").all()
    filterset_class = ExpressionFilter


@document_bulk_create(ParameterSerializer, name="parameters")
class ParameterViewSet(KoraViewSet):
    queryset = Parameter.objects.all()
    serializer_class = ParameterSerializer
    filterset_class = ParameterFilter


@document_bulk_create(VarietalParameterSerializer, name="varietalparameters")
class VarietalParameterViewSet(KoraViewSet):
    queryset = VarietalParameter.objects.select_related("parameter").all()
    serializer_class = VarietalParameterSerializer
    filterset_class = VarietalParameterFilter


@document_bulk_create(StorageSerializer, name="storages")
class StorageViewSet(KoraViewSet):
    queryset = Storage.objects.all()
    serializer_class = StorageSerializer
    filterset_class = StorageFilter


@document_bulk_create(StoragePositionSerializer, name="storagepositions")
class StoragePositionViewSet(KoraViewSet):
    queryset = StoragePosition.objects.select_related("storage")
    serializer_class = StoragePositionSerializer
    filterset_class = StoragePositionFilter


@document_bulk_create(SampleSerializer, name="samples")
class SampleViewSet(KoraViewSet):
    queryset = Sample.objects.with_availability().with_germination()
    serializer_class = SampleSerializer
    filterset_class = SampleFilter


@document_bulk_create(SampleWeightSerializer, name="sampleweights")
class SampleWeightViewSet(KoraViewSet):
    queryset = SampleWeight.objects.select_related("sample").all()
    serializer_class = SampleWeightSerializer
    filterset_class = SampleWeightFilter


@document_bulk_create(GerminabilitySerializer, name="germinabilities")
class GerminabilityViewSet(KoraViewSet):
    queryset = Germinability.objects.select_related("sample").all()
    serializer_class = GerminabilitySerializer
    filterset_class = GerminabilityFilter


class CartItemViewSet(KoraViewSet):
    serializer_class = CartItemSerializer

    def get_queryset(self):
        if getattr(self, "swagger_fake_view", False):
            return CartItem.objects.none()

        user = self.request.user
        cart = self.kwargs["cart"]
        return CartItem.objects.select_related(
            "sample__variety__species",
            "sample__position__storage",
        ).filter(cart__user=user, cart__pk=cart)

    def get_cart(self):
        return get_object_or_404(Cart.objects.filter(user=self.request.user), pk=self.kwargs["cart"])

    def perform_create(self, serializer):
        serializer.save(cart=self.get_cart())

    def perform_bulk_create(self, serializer):
        serializer.save(cart=self.get_cart())


class CartViewSet(viewsets.ModelViewSet):
    serializer_class = CartSerializer

    def get_queryset(self):
        if getattr(self, "swagger_fake_view", False):
            return Cart.objects.none()

        return Cart.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class WorkspaceViewSet(viewsets.ModelViewSet):
    serializer_class = WorkspaceSerializer

    def get_queryset(self):
        if getattr(self, "swagger_fake_view", False):
            return Workspace.objects.none()

        return Workspace.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class WorkspaceElementViewSet(KoraViewSet):
    serializer_class = WorkspaceElementSerializer

    def get_queryset(self):
        if getattr(self, "swagger_fake_view", False):
            return WorkspaceElement.objects.none()

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

    def get_workspace(self):
        return get_object_or_404(
            Workspace,
            pk=self.kwargs["workspace"],
            user=self.request.user,
        )

    def perform_create(self, serializer):
        serializer.save(workspace=self.get_workspace())

    def perform_bulk_create(self, serializer):
        serializer.save(workspace=self.get_workspace())
