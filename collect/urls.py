from django.urls import path

from . import views

app_name = "collect"

urlpatterns = [
    path("", views.SeedSamplesList.as_view(), name="seedsamples-list"),
    path("create", views.seedsample_create, name="seedsamples-create"),
]
