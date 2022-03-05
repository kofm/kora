from django.urls import path

from . import views

app_name = "calculator"

urlpatterns = [
    path("", views.calculator, name="calculator"),
    path("fetcharea", views.fetch_area, name="fetch-area"),
]
