from django.urls import path

from . import views

app_name = "spaces"

urlpatterns = [
        path('locations', views.LocationList.as_view(), name='locations_list'),
        path('locations/<int:pk>', views.LocationDetail.as_view(), name='locations_detail')
        ]
