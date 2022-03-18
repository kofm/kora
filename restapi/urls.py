from django.urls import include, path
from rest_framework import routers

from . import views
from collect.views import SeedSampleViewSet

app_name = "restapi"

router = routers.DefaultRouter()
router.register(r"crops", views.CropViewSet)
router.register(r"varieties", views.PlantVarietyViewSet)
router.register(r"seedsample", SeedSampleViewSet)

urlpatterns = [
    path("", include(router.urls)),
]
