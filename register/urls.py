from django.urls import path

from . import views

urlpatterns = [
        path('', views.index, name = 'index'),
        path('species/', views.PlantSpeciesList.as_view()),
        path('species/<int:pk>', views.PlantSpeciesDetail.as_view(), name='plantspecie_detail'),
        path('variety/<int:pk>', views.PlantVarietyDetail.as_view(), name='variety_detail')
]
