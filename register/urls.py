from django.urls import path

from . import views

app_name = "register"

urlpatterns = [
    path("species/", views.PlantSpeciesList.as_view(), name="species_list"),
    path("species/create", views.PlantSpeciesCreate.as_view(), name="species_create"),
    path(
        "species/<int:pk>",
        views.PlantSpeciesDetail.as_view(),
        name="plantspecie_detail",
    ),
    path(
        "species/<int:pk>/parameters",
        views.PlantSpeciesParametersList.as_view(),
        name="plantspeciesparameters_list",
    ),
    path(
        "species/<int:pk>/parameters/create",
        views.add_cropparametervervalue,
        name="add_cropparamval",
    ),
    path("variety/<int:pk>", views.PlantVarietyDetail.as_view(), name="variety_detail"),
    path(
        "variety/<int:pk>/parameters",
        views.PlantVarietyParametersList.as_view(),
        name="plantvarietyparameters_list",
    ),
    path(
        "variety/<int:pk>/parameters/create",
        views.add_varietalparamevterervalue,
        name="add_varparamval",
    ),
]
