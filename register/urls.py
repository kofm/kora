from django.urls import path

from . import views

app_name = 'register'

urlpatterns = [
        path('species/', views.PlantSpeciesList.as_view(), name='species_list'),
        path('species/create', views.PlantSpeciesCreate.as_view(), name='species_create'),
        path('species/<int:pk>', views.PlantSpeciesDetail.as_view(), name='plantspecie_detail'),
        path('variety/<int:pk>', views.PlantVarietyDetail.as_view(), name='variety_detail'),
]
