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
    EntityImportSerializer,
    PlantVarietyImportSerializer,
    ProtectionExcelImportSerializer,
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
    @action(detail=False, methods=["post"], serializer_class=PlantVarietyImportSerializer)
    def excel_import(self, request):
        """Import varieties from an Excel table.

        **Accepted columns**:

        - ``name`` (required, string): the denomination of the variety;
        - ``species_id`` (required, integer): the I of the species (see
          :http:get:`/api/species/`);

        NOTE: if a variety of the same species with the same name
        already exists, it will not be imported. If you really need a
        variety with the same name you will have to add it through the
        user interface.

        """
        return super().excel_import(request)


@document_bulk_create(EntitySerializer, name="entities")
class EntityViewSet(ExcelImportActionMixin, KoraViewSet):
    queryset = Entity.objects.all()
    serializer_class = EntitySerializer
    filterset_class = EntityFilter
    excel_import_serializer_class = EntityImportSerializer

    def perform_excel_import_create(self, objs):
        created = Entity.objects.bulk_create([obj for obj in objs if obj], batch_size=1000)
        return len(created)

    @extend_schema(responses=ExcelImportResponseSerializer)
    @action(detail=False, methods=["post"], serializer_class=EntityImportSerializer)
    def excel_import(self, request):
        """Import entities from an Excel table.


        **Accepted columns**

        - ``name`` (text, required): the entity name;
        - ``type`` (text, optional): type of entity, one of ``IN``
          (Individual), ``PA`` (Partnership), ``CO`` (Company), ``CP``
          (Cooperative);
        - ``country`` (text, optional): ISO 3166-1 two-letter country code;
        - ``contact`` (text, optional): contact information;
        - ``email`` (text, optional): email address.
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

    @extend_schema(responses=ExcelImportResponseSerializer)
    @action(detail=False, methods=["post"], serializer_class=ProtectionExcelImportSerializer)
    def excel_import(self, request):
        """Import protections from an Excel table.

        **Accepted columns**:

        - ``name`` (text, required): name of the variety - this will be
          matched with existing varieties of the specified species_id,
          and will throw an error when no matches are found;
        - ``species_id`` (integer, required): the ID of the variety's
          species (see :http:get:`/api/species/`);
        - ``type`` (text, required): protection type, the three letter
          code identifying the protection type (see
          :http:get:`/api/protection_types/`);
        - ``reference`` (text, optional): arbitrary reference
          number/code (e.g. application number)
        - ``status`` (text, optional): protection status, one of ``G``
          (Granted), ``T`` (Terminated), ``A`` (Active Application), ``W``
          (Withdrawn), ``R`` (Refused), ``S`` (Surrendered);
        - ``country`` (text, optional): ISO 3166-1 two-letter country code;
        - ``date_start`` (date, optional): start date of the protection
          (YMD format);
        - ``date_end`` (date, optional): end date of the protection (YMD
          format);
        - ``applicants`` (array, optional): semi-colon separated list of
          applicant names
        - ``maintainers`` (array, optional): semi-colon separated list
          of maintainer names
        - ``note`` (text, optional): additional information

        The ``applicants`` and ``maintainers`` columns in the protection
        import file allow multiple entities. These should be entered
        as semi-colon separated names (e.g. `"Entity A; Entity
        B"`). This format is commonly used by many public
        databases. Avoid using semi-colon separated names in the
        entities import file, as these will be imported as a single
        entity.

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
    queryset = StoragePosition.objects.all()
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
        return Cart.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class WorkspaceViewSet(viewsets.ModelViewSet):
    serializer_class = WorkspaceSerializer

    def get_queryset(self):
        return Workspace.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class WorkspaceElementViewSet(KoraViewSet):
    serializer_class = WorkspaceElementSerializer
    jsonl_export_filename = "workspace"

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

    def get_workspace(self):
        return get_object_or_404(Workspace.objects.get(pk=self.kwargs["workspace"], user=self.request.user))

    def perform_create(self, serializer):
        serializer.save(workspace=self.get_workspace())

    def perform_bulk_create(self, serializer):
        serializer.save(workspace=self.get_workspace())
