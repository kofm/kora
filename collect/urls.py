from django.urls import path

from . import views

app_name = "collect"

urlpatterns = [
    path("", views.SeedSampleListView.as_view(), name="seedsamples-list"),
    path("sample/<int:pk>", views.SeedSampleDetailView.as_view(), name="seedsample-detail"),
    path("sample/<int:pk>/update", views.SeedSampleUpdateView.as_view(), name="seedsample-update"),
    path("sample/create", views.SeedSampleCreateView.as_view(), name="seedsample-create"),
    path("sample/<int:pk>/delete", views.SeedSampleDeleteView.as_view(), name="seedsample-delete"),
    path("storage/create", views.StorageCreateView.as_view(), name="storage-create"),
    path("storage", views.StorageListView.as_view(), name="storage-list"),
    path("germinability", views.germinability, name="germinability"),
    path("sample/<int:pk>/germinability/create", views.GerminabilityCreateView.as_view(), name="germinability-create"),
    path("sample/<int:pk>/sampleweight/create", views.SampleWeightCreateView.as_view(), name="sampleweight-create"),
    path("germinability/<int:pk>/delete", views.GerminabilityDeleteView.as_view(), name="germinability-delete"),
    path("sampleweight", views.sample_weight, name="sample-weight"),
]
