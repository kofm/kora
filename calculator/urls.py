from django.urls import path

from . import views

app_name = "calculator"

urlpatterns = [
    path("calculator", views.description_manage, name="description-manage"),
]
