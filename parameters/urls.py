from django.urls import path

from . import views

app_name = "parameters"

urlpatterns = [
    path("", views.parameter_list, name="parameter_list"),
    path("autocomplete", views.ParameterAutocompleteView.as_view(), name="parameter_autocomplete"),
    path("create", views.ParameterCreate.as_view(), name="parameter_create"),
    path("<int:pk>", views.parameter_detail, name="parameter_detail"),
    path("<int:pk>/update", views.ParameterUpdate.as_view(), name="parameter_update"),
    path("<int:pk>/delete", views.ParameterDelete.as_view(), name="parameter_delete"),
    path("varietalparameters", views.varietalparameter_list, name="varietalparameter_list"),
    path("varietalparameters/create", views.varietalparameter_create, name="varietalparameter_create"),
    path("varietalparameters/<int:pk>/update", views.varietalparameter_update, name="varietalparameter_update"),
    path("varietalparameters/<int:pk>/delete", views.varietalparameter_delete, name="varietalparameter_delete"),
]
