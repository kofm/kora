from django.urls import include, path
from rest_framework import routers

from . import views

app_name = "restapi"

router = routers.DefaultRouter()
router.register(r"species", views.PlantSpeciesViewSet)
router.register(r"varieties", views.PlantVarietyViewSet)
router.register(r"entities", views.EntityViewSet)
router.register(r"protections", views.ProtectionViewSet, basename="protection")
router.register(r"protocols", views.ProtocolViewSet, basename="protocols")
router.register(r"traits", views.TraitViewSet, basename="traits")
router.register(r"states", views.StateViewSet, basename="states")
router.register(r"descriptions", views.DescriptionViewSet, basename="descriptions")
router.register(r"parameters", views.ParameterViewSet)
router.register(r"varietalparameters", views.VarietalParameterViewSet)
router.register(r"storages", views.StorageViewSet)
router.register(r"storagepositions", views.StoragePositionViewSet)
router.register(r"samples", views.SampleViewSet)
router.register(r"sampleweights", views.SampleWeightViewSet)
router.register(r"workspaces", views.WorkspaceViewSet, basename="workspace")
router.register(r"carts", views.CartViewSet, basename="cart")

urlpatterns = [
    path("", include(router.urls)),
    path("<int:cart>/cartitems/", views.CartItemViewSet.as_view({"get": "list", "post": "create"}), name="cartitems"),
    path("<int:workspace>/workspaces/", views.WorkspaceElementViewSet.as_view({"get": "list"}), name="workspaces"),
]
