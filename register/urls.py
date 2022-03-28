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
        views.add_speciesparametervervalue,
        name="add_cropparamval",
    ),
    path("variety/<int:pk>", views.PlantVarietyDetail.as_view(), name="variety_detail"),
    path(
        "species/<int:pk>/variety/create",
        views.plantvariety_create,
        name="plantvariety-create",
    ),
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
    path(
        "variety/<int:pk>/delete",
        views.PlantVarietyDelete.as_view(),
        name="plantvariety-delete",
    ),
    path(
        "variety/name/<int:pk>/delete",
        views.PlantVarietyNameDelete.as_view(),
        name="plantvarietyname-delete"
    ),
    path(
        "variety/<int:pk>/name/create",
        views.PlantVarietyNameCreate.as_view(),
        name="plantvarietyname-create"
    ),
    path(
        "variety/name/<int:pk>/update",
        views.PlantVarietyNameUpdate.as_view(),
        name="plantvarietyname-update"
    )
]
