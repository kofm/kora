from django.urls import path

from . import views

app_name = "spaces"

urlpatterns = [
    path("locations", views.LocationListView.as_view(), name="location-list"),
    path("area/sort_hx", views.area_sort_hx, name="area-sort"),
    path("area/<int:pk>", views.AreaDetailView.as_view(), name='area-detail'),
    path("area/<int:pk>/delete", views.AreaDeleteView.as_view(), name='area-delete'),
    path("area/<int:pk>/update", views.AreaUpdateView.as_view(), name='area-update'),
    path("location/<int:location_id>/area/create", views.AreaCreateView.as_view(), name='area-create'),
    path("locations/<int:pk>", views.location_detail, name='location-detail'),
    path("location/<int:pk>/update", views.LocationUpdateView.as_view(), name='location-update'),
    path("location/<int:pk>/delete", views.LocationDeleteView.as_view(), name='location-delete'),
    path("location/create", views.LocationCreateView.as_view(), name='location-create'),
    path("area/<int:pk>/duplicate", views.area_duplicate, name='area-duplicate'),
    path("test", views.test, name='test'),
]
