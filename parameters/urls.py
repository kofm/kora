from django.urls import path

from . import views

app_name = 'parameters'

urlpatterns = [
        path('', views.ParametersList.as_view(), name = 'parameters-list'),
        path('create', views.ParameterCreate.as_view(), name = 'parameter-create'),
        path('<int:pk>', views.ParameterDetail.as_view(), name = 'parameter-detail'),
        path('<int:pk>/update', views.ParameterUpdate.as_view(), name = 'parameter-update'),
        path('<int:pk>/delete', views.ParameterDelete.as_view(), name = 'parameter-delete'),
        path('cropparam/<int:pk>/update', views.CropParameterUpdate.as_view(), name = 'cropparam-update')
]

