from django.urls import include, path
from rest_framework import routers

from . import views

app_name = "restapi"

router = routers.DefaultRouter()
router.register(r"species", views.PlantSpeciesViewSet)
router.register(r"varieties", views.PlantVarietyViewSet)
router.register(r"entities", views.EntityViewSet)
router.register(r"protections", views.ProtectionViewSet)
router.register(r"varietalparameters", views.VarietalParameterViewSet)
router.register(r"seedsamples", views.SeedSampleViewSet)
router.register(r"storagepositions", views.StoragePositionViewSet)
router.register(r"protocols", views.ProtocolViewSet, basename="protocols")
router.register(r"traits", views.TraitViewSet, basename="traits")
router.register(r"states", views.StateViewSet, basename="states")
router.register(r"descriptions", views.DescriptionViewSet, basename="descriptions")
router.register(r"expressions", views.ExpressionViewSet, basename="expressions")

urlpatterns = [
    path("", include(router.urls)),
    path("<int:cart>/cartitems/", views.CartItemViewSet.as_view({"get": "list"}), name="cartitems"),
]
