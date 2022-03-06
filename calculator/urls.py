from django.urls import path

from . import views

app_name = "calculator"

urlpatterns = [
    path("", views.calculator, name="calculator"),
    path("fetcharea", views.fetch_area, name="fetch-area"),
    path("fetchspecies", views.fetch_species, name="fetch-species"),
    path("create", views.store, name="store-crop"),
]
