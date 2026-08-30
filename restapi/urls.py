from django.urls import include, path
from drf_spectacular.views import SpectacularAPIView
from rest_framework.routers import APIRootView, DefaultRouter

from . import views

app_name = "restapi"


class KoraAPIRootView(APIRootView):
    name = "Kora API"


class KoraDefaultRouter(DefaultRouter):
    APIRootView = KoraAPIRootView


router = KoraDefaultRouter()
router.register(r"species", views.PlantSpeciesViewSet)
router.register(r"varieties", views.PlantVarietyViewSet)
router.register(r"entities", views.EntityViewSet, basename="entities")
router.register(r"protections", views.ProtectionViewSet, basename="protections")
router.register(r"protection_types", views.ProtectionTypeViewSet, basename="protection_types")
router.register(r"protocols", views.ProtocolViewSet, basename="protocols")
router.register(r"traits", views.TraitViewSet, basename="traits")
router.register(r"states", views.StateViewSet, basename="states")
router.register(r"descriptions", views.DescriptionViewSet, basename="descriptions")
router.register(r"expressions", views.ExpressionViewSet, basename="expressions")
router.register(r"parameters", views.ParameterViewSet)
router.register(r"varietalparameters", views.VarietalParameterViewSet)
router.register(r"storages", views.StorageViewSet)
router.register(r"storagepositions", views.StoragePositionViewSet)
router.register(r"samples", views.SampleViewSet)
router.register(r"sampleweights", views.SampleWeightViewSet)
router.register(r"germinabilities", views.GerminabilityViewSet)
router.register(r"workspaces", views.WorkspaceViewSet, basename="workspaces")
router.register(r"carts", views.CartViewSet, basename="cart")
router.register(r"crop-layouts", views.CropLayoutViewSet, basename="crop-layout")
router.register(r"crops", views.CropViewSet, basename="crops")
router.register("fieldbooks", views.FieldBookViewSet, basename="fieldbooks")
router.register(r"trait-targets", views.TraitTargetViewSet, basename="trait-targets")
router.register(r"parameter-targets", views.ParameterTargetViewSet, basename="parameter-targets")
router.register(r"trait-observations", views.TraitObservationViewSet, basename="trait-observations")
router.register(r"parameter-observations", views.ParameterObservationViewSet, basename="parameter-observations")

urlpatterns = [
    path("schema/", SpectacularAPIView.as_view(), name="schema"),
    path("", include(router.urls)),
    path("<int:cart>/cartitems/", views.CartItemViewSet.as_view({"get": "list", "post": "create"}), name="cartitems"),
    path(
        "<int:cart>/cartitems/export-jsonl/",
        views.CartItemViewSet.as_view({"get": "export_jsonl"}),
        name="cartitems-export",
    ),
    path("<int:cart>/cartitems/bulk/", views.CartItemViewSet.as_view({"post": "bulk"}), name="cartitems-bulk"),
    path(
        "workspaces/<int:workspace>/elements/",
        views.WorkspaceElementViewSet.as_view({"get": "list", "post": "create"}),
        name="workspaceelements",
    ),
    path(
        "workspaces/<int:workspace>/elements/export-jsonl/",
        views.WorkspaceElementViewSet.as_view({"get": "export_jsonl"}),
        name="workspaceelements-export",
    ),
]
