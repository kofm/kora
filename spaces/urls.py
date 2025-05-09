from django.urls import path

from . import views

app_name = "spaces"

urlpatterns = [
    path("locations", views.location_list, name="location_list"),
    path("locations/sort", views.SortLocation.as_view(), name="location_sort"),
    path("locations/<int:location_id>/area/create", views.area_create, name="area_create"),
    path("locations/<int:pk>", views.location_detail, name="location_detail"),
    path("locations/<int:pk>/update", views.LocationUpdateView.as_view(), name="location_update"),
    path("locations/<int:pk>/delete", views.LocationDeleteView.as_view(), name="location_delete"),
    path("locations/create", views.LocationCreateView.as_view(), name="location_create"),
    path("areas/sort", views.AreaSort.as_view(), name="area_sort"),
    path("areas/<int:pk>", views.area_detail, name="area_detail"),
    path("areas/<int:pk>/update", views.AreaUpdateView.as_view(), name="area_update"),
    path("areas/<int:pk>/delete", views.AreaDeleteView.as_view(), name="area_delete"),
    path("areas/<int:pk>/duplicate", views.area_duplicate, name="area_duplicate"),
]
