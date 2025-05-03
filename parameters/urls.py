from django.urls import path

from register.views import VarietalParameterCreate

from . import views

app_name = "parameters"

urlpatterns = [
    path("", views.parameter_list, name="parameter_list"),
    path("create", views.ParameterCreate.as_view(), name="parameter_create"),
    path("<int:pk>", views.ParameterDetail.as_view(), name="parameter-detail"),
    path("<int:pk>/update", views.ParameterUpdate.as_view(), name="parameter-update"),
    path("<int:pk>/delete", views.ParameterDelete.as_view(), name="parameter-delete"),
    path(
        "variety/<int:pk>/create",
        VarietalParameterCreate.as_view(),
        name="varietalparameter_create",
    ),
    path("varietalparameter/<int:pk>/update", views.varietalparameter_update, name="varietalparameter-update"),
    path("varietalparameter/<int:pk>/delete", views.varietalparameter_delete, name="varietalparameter-delete"),
    path(
        "cropparam/<int:pk>/update",
        views.SpeciesParameterUpdate.as_view(),
        name="cropparam-update",
    ),
]
