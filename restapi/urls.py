from django.urls import include, path
from rest_framework import routers
from . import views

app_name = 'restapi'

router = routers.DefaultRouter()
router.register(r'crops', views.CropViewSet)

urlpatterns = [
    path('', include(router.urls)),
]


