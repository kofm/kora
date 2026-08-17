from django.urls import path

from . import views

app_name = "spaces"

urlpatterns = [
    path("locations", views.location_list, name="location_list"),
    path("locations/autocomplete", views.LocationAutocompleteView.as_view(), name="location_autocomplete"),
    path("locations/<int:pk>", views.location_detail, name="location_detail"),
    path("locations/create", views.location_create, name="location_create"),
    path("locations/<int:pk>/update", views.LocationUpdateView.as_view(), name="location_update"),
    path("locations/<int:pk>/delete", views.location_delete, name="location_delete"),
    path("locations/sort", views.SortLocation.as_view(), name="location_sort"),
]
