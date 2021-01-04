from django.urls import path
from . import views

app_name = 'describe'

urlpatterns = [
        path('', views.DescriptionsList.as_view(), name= 'descriptions_list'),
        path('<int:pk>/', views.DescriptionDetail.as_view(), name='description_detail'),
        path('protocols/', views.ProtocolsList.as_view(), name='protocols_list'),
        path('protocols/<int:pk>/', views.ProtocolDetail.as_view(), name = 'protocol_detail'),
]
