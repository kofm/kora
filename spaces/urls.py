from django.urls import path

from . import views

app_name = "spaces"

urlpatterns = [
    path("locations", views.LocationListView.as_view(), name="location-list"),
    path("locations/<int:pk>", views.LocationDetailView.as_view(), name='location-detail'),
    path("locations/area/<int:pk>", views.AreaDetailView.as_view(), name='area-detail'),
    path("locations/area/<int:pk>/update", views.AreaUpdateView.as_view(), name='area-update'),
]
