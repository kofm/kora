from django.urls import path

from . import views

app_name = 'parameters'

urlpatterns = [
        path('', views.ParametersList.as_view(), name = 'parameters_list'),
        path('create', views.ParametersCreate.as_view(), name = 'parameters_create')
]

