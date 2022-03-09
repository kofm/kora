from django.urls import path

from . import views

app_name = "collect"

urlpatterns = [
    path("", views.SeedSampleListView.as_view(), name="seedsamples-list"),
    path("sample/<int:pk>", views.SeedSampleDetailView.as_view(), name="seedsample-detail"),
    path("sample/update/<int:pk>", views.SeedSampleUpdateView.as_view(), name="seedsample-update"),
    path("sample/create", views.SeedSampleCreateView.as_view(), name="seedsample-create"),
    path("sample/delete/<int:pk>", views.SeedSampleDeleteView.as_view(), name="seedsample-delete"),
    path("storage/create", views.StorageCreateView.as_view(), name="storage-create"),
    path("storageposition/<int:pk>", views.fetch_storagepositions, name="fetch-storagepositions"),
    path("germinability", views.germinability, name="germinability"),
    path("sampleweight", views.sample_weight, name="sample-weight"),
]
