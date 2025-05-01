from django.urls import path

from . import views

app_name = "register"

urlpatterns = [
    path("species/create", views.PlantSpeciesCreate.as_view(), name="plantspecies_create"),
    path("species/", views.PlantSpeciesList.as_view(), name="plantspecies_list"),
    path("species/<int:pk>", views.PlantSpeciesDetailView.as_view(), name="plantspecies_detail"),
    path("species/<int:pk>/update", views.PlantSpeciesUpdateView.as_view(), name="plantspecies_update"),
    path("species/<int:pk>/delete", views.PlantSpeciesDeleteView.as_view(), name="plantspecies_delete"),
    path("varieties", views.plantvariety_list, name="variety_list"),
    path("varieties/<int:pk>", views.plantvariety_detail, name="variety_detail"),
    path("varieties/create", views.PlantVarietyCreate.as_view(), name="variety_create"),
    path("varieties/<int:pk>/update", views.PlantVarietyUpdateView.as_view(), name="variety_update"),
    path("varieties/<int:pk>/delete", views.PlantVarietyDelete.as_view(), name="variety_delete"),
    path("varieties/<int:pk>/parameters", views.PlantVarietyParametersList.as_view(), name="parameter_list"),
    path("varieties/name/<int:pk>/delete", views.plantvarietyname_delete, name="denomination_delete"),
    path("varieties/<int:pk>/name/create", views.plantvarietyname_create, name="denomination_create"),
    path("varieties/name/<int:pk>/update", views.plantvarietyname_update, name="denomination_update"),
    path("protections/", views.protection_list, name="protection_list"),
    path("protections/<int:pk>", views.protection_detail, name="protection_detail"),
    path("varieties/<int:variety_id>/protections/create", views.protection_create, name="protection_create"),
    path("protections/<int:pk>/update", views.protection_update, name="protection_update"),
    path("protections/<int:pk>/delete", views.ProtectionDeleteView.as_view(), name="protection_delete"),
    path("entities/", views.entity_list, name="entity_list"),
    path("entities/<int:pk>", views.entity_detail, name="entity_detail"),
    path("entity/create", views.EntityCreateView.as_view(), name="entity_create"),
    path("entities/<int:pk>/update", views.EntityUpdateView.as_view(), name="entity_update"),
    path("entities/<int:pk>/delete", views.EntityDeleteView.as_view(), name="entity_delete"),
]
