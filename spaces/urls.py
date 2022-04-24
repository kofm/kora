from django.urls import path

from . import views

app_name = "spaces"

urlpatterns = [
    path("locations", views.LocationListView.as_view(), name="location-list"),
    path("locations/<int:pk>", views.LocationDetailView.as_view(), name='location-detail'),
    path("area/<int:pk>", views.AreaDetailView.as_view(), name='area-detail'),
    path("area/<int:pk>/delete", views.AreaDeleteView.as_view(), name='area-delete'),
    path("area/<int:pk>/update", views.AreaUpdateView.as_view(), name='area-update'),
    path("location/<int:location_id>/area/create", views.AreaCreateView.as_view(), name='area-create'),
]
