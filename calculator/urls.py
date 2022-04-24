from django.urls import path

from . import views

app_name = "calculator"

urlpatterns = [
    path("crop/<int:pk>", views.CropDetailView.as_view(), name="crop-detail"),
    path("area/<int:area_id>/crop/create", views.CropCreateView.as_view(), name="crop-create-area"),
    path("crop/create", views.CropCreateView.as_view(), name="crop-create"),
    path("crop/<int:pk>/update", views.crop_update_view, name="crop-update"),
    path("crop/<int:pk>/management/create", views.ManagementCreateView.as_view(), name="management-create"),
    path("crop/<int:pk>/delete", views.CropDeleteView.as_view(), name="crop-delete"),
]
