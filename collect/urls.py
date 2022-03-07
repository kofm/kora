from django.urls import path

from . import views

app_name = "collect"

urlpatterns = [
    path("", views.SeedSampleListView.as_view(), name="seedsamples-list"),
    path("sample/<int:pk>", views.SeedSampleDetailView.as_view(), name="seedsample-detail"),
    path("create", views.seedsample_create, name="seedsamples-create"),
]
