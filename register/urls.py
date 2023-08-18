from describe import views as describe_views
from django.urls import path

from . import views

app_name = "register"

urlpatterns = [
    path("species/", views.PlantSpeciesList.as_view(), name="plantspecies-list"),
    path(
        "species/create", views.PlantSpeciesCreate.as_view(), name="plantspecies-create"
    ),
    path(
        "species/<int:pk>",
        views.PlantSpeciesDetailView.as_view(),
        name="plantspecies-detail",
    ),
    path(
        "species/<int:pk>/update",
        views.PlantSpeciesUpdateView.as_view(),
        name="plantspecies-update",
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
    path(
        "variety/<int:pk>",
        views.PlantVarietyDetail.as_view(),
        name="plantvariety-detail",
    ),
    path(
        "species/<int:species_id>/variety/create",
        views.PlantVarietyCreate.as_view(),
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
        name="plantvarietyname-delete",
    ),
    path(
        "variety/<int:pk>/name/create",
        views.PlantVarietyNameCreate.as_view(),
        name="plantvarietyname-create",
    ),
    path(
        "variety/name/<int:pk>/update",
        views.PlantVarietyNameUpdate.as_view(),
        name="plantvarietyname-update",
    ),
    path(
        "species/<int:species_id>/protocols",
        describe_views.protocol_list,
        name="protocol-list",
    ),
    path(
        "protection/<int:pk>",
        views.ProtectionDetailView.as_view(),
        name="protection-detail",
    ),
    path(
        "protection/<int:pk>/update", views.protection_update, name="protection-update"
    ),
    path(
        "variety/<int:variety_id>/protection/create",
        views.protection_create,
        name="protection-create",
    ),
    path("entity/create", views.EntityCreateView.as_view(), name="entity-create"),
    path("entity/", views.entity_list, name="entity-list"),
    path("entity/<int:pk>", views.entity_detail, name="entity-detail"),
    path(
        "entity/<int:pk>/update", views.EntityUpdateView.as_view(), name="entity-update"
    ),
    path(
        "variety/<int:pk>/update",
        views.PlantVarietyUpdateView.as_view(),
        name="plantvariety-update",
    ),
]
