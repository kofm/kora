from django.urls import include, path
from rest_framework import routers

from . import views

app_name = "restapi"

router = routers.DefaultRouter()
router.register(r"species", views.CropViewSet)
router.register(r"varieties", views.PlantVarietyViewSet)
router.register(r"entities", views.EntityViewSet)
router.register(r"protections", views.ProtectionViewSet)
router.register(r"varietalparameters", views.VarietalParameterViewSet)

urlpatterns = [
    path("", include(router.urls)),
]
