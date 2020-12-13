from django.urls import path

from . import views

app_name = 'register'

urlpatterns = [
        path('', views.index, name = 'index'),
        path('species/', views.PlantSpeciesList.as_view(), name='species_list'),
        path('species/<int:pk>', views.PlantSpeciesDetail.as_view(), name='plantspecie_detail'),
        path('variety/<int:pk>', views.PlantVarietyDetail.as_view(), name='variety_detail')
]
