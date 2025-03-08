from django.urls import path

from . import views

app_name = "front"

urlpatterns = [
    path("", views.index, name="index"),
    path("appearance/set", views.appearance_set, name="appearance_set"),
]
