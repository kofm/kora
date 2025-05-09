from django.urls import path

from . import views

app_name = "spaces"

urlpatterns = [
    path("locations", views.location_list, name="location_list"),
    path("locations/sort", views.SortLocation.as_view(), name="location-sort"),
    path("area/sort", views.AreaSort.as_view(), name="area-sort"),
    path("area/<int:pk>", views.area_detail, name="area-detail"),
    path("area/<int:pk>/delete", views.AreaDeleteView.as_view(), name="area-delete"),
    path("area/<int:pk>/update", views.AreaUpdateView.as_view(), name="area-update"),
    path("location/<int:location_id>/area/create", views.area_create, name="area-create"),
    path("locations/<int:pk>", views.location_detail, name="location-detail"),
    path(
        "location/<int:pk>/update",
        views.LocationUpdateView.as_view(),
        name="location-update",
    ),
    path(
        "location/<int:pk>/delete",
        views.LocationDeleteView.as_view(),
        name="location-delete",
    ),
    path("location/create", views.LocationCreateView.as_view(), name="location-create"),
    path("area/<int:pk>/duplicate", views.area_duplicate, name="area-duplicate"),
]
