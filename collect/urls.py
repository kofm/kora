from django.urls import path

from . import views

app_name = "collect"

urlpatterns = [
    path("", views.SeedSampleListView.as_view(), name="seedsample-list"),
    path("sample/<int:pk>", views.SeedSampleDetailView.as_view(), name="seedsample-detail"),
    path("sample/<int:pk>/update", views.SeedSampleUpdateView.as_view(), name="seedsample-update"),
    path("sample/<int:pk>/delete", views.SeedSampleDeleteView.as_view(), name="seedsample-delete"),
    path("sampleweight/<int:pk>/delete", views.SeedSampleDetailView.as_view(), name="sampleweight-delete"),
    path("sampleweight/<int:pk>/create", views.sampleweight_create_hx, name="sampleweight-create"),
    path("germinability/<int:pk>/delete", views.SeedSampleDetailView.as_view(), name="germinability-delete"),
    path("germinability/<int:pk>/create", views.SeedSampleDetailView.as_view(), name="germinability-create"),
]
