from django.urls import path

from . import views

app_name = "register"

urlpatterns = [
    path("species/create", views.PlantSpeciesCreate.as_view(), name="plantspecies_create"),
    path("species/", views.PlantSpeciesList.as_view(), name="plantspecies_list"),
    path(
        "species/<int:pk>",
        views.PlantSpeciesDetailView.as_view(),
        name="plantspecies_detail",
    ),
    path(
        "species/<int:pk>/update",
        views.PlantSpeciesUpdateView.as_view(),
        name="plantspecies_update",
    ),
    path(
        "species/<int:pk>/delete",
        views.PlantSpeciesDeleteView.as_view(),
        name="plantspecies_delete",
    ),
    path(
        "variety/<int:pk>",
        views.PlantVarietyDetail.as_view(),
        name="plantvariety_detail",
    ),
    path(
        "variety/create",
        views.PlantVarietyCreate.as_view(),
        name="variety_create",
    ),
    path(
        "variety/<int:pk>/parameters",
        views.PlantVarietyParametersList.as_view(),
        name="plantvarietyparameters_list",
    ),
    path(
        "variety/<int:pk>/delete",
        views.PlantVarietyDelete.as_view(),
        name="variety_delete",
    ),
    path(
        "variety/name/<int:pk>/delete",
        views.plantvarietyname_delete,
        name="denomination_delete",
    ),
    path(
        "variety/<int:pk>/name/create",
        views.plantvarietyname_create,
        name="denomination_create",
    ),
    path(
        "variety/name/<int:pk>/update",
        views.plantvarietyname_update,
        name="denomination_update",
    ),
    path("protections/", views.protection_list, name="protection_list"),
    path("protection/<int:pk>", views.protection_detail, name="protection_detail"),
    path("protection/<int:pk>/update", views.protection_update, name="protection_update"),
    path("protection/<int:pk>/delete", views.ProtectionDeleteView.as_view(), name="protection_delete"),
    path(
        "variety/<int:variety_id>/protection/create",
        views.protection_create,
        name="protection-create",
    ),
    path("entity/create", views.EntityCreateView.as_view(), name="entity_create"),
    path("entity/", views.entity_list, name="entity_list"),
    path("entity/<int:pk>", views.entity_detail, name="entity_detail"),
    path("entity/<int:pk>/update", views.EntityUpdateView.as_view(), name="entity_update"),
    path("entity/<int:pk>/delete", views.EntityDeleteView.as_view(), name="entity_delete"),
    path(
        "variety/<int:pk>/update",
        views.PlantVarietyUpdateView.as_view(),
        name="variety_update",
    ),
    path("varieties", views.plantvariety_list, name="variety_list"),
]
