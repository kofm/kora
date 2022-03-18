from django.urls import path

from . import views

app_name = "calculator"

urlpatterns = [
    path("", views.index, name="calculator"),
    path("fetcharea/<int:pk>", views.fetch_area, name="fetch-area"),
    path("crop/<int:pk>", views.CropDetailView.as_view(), name="crop-detail"),
    path("crop/<int:pk>/delete", views.CropDeleteView.as_view(), name="crop-delete"),
    path("fetchspecies", views.fetch_species, name="fetch-species"),
    path("create", views.store, name="store-crop"),
]
