from django.urls import path

from . import views

app_name = "calculator"

urlpatterns = [
    path("", views.index, name="calculator"),
    path("fetcharea/<int:pk>", views.fetch_area, name="fetch-area"),
    path("cropparameter/<int:pk>", views.cropparameter_detail, name="cropparameter-detail"),
    path("cropparameter", views.cropparameter_list, name="cropparameter-list"),
    path("crop/<int:pk>", views.CropDetailView.as_view(), name="crop-detail"),
    path("crop/<int:pk>/update", views.CropUpdateView.as_view(), name="crop-update"),
    path("crop/<int:pk>/management/create", views.ManagementCreateView.as_view(), name="management-create"),
    path("cropparameter/update", views.cropparameter_update, name="cropparameter-update"),
    path("<int:pk>/delete", views.CropDeleteView.as_view(), name="crop-delete"),
    path("fetchspecies", views.fetch_species, name="fetch-species"),
    path("create", views.store, name="store-crop"),
]
