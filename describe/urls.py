from django.urls import path
from . import views

app_name = 'describe'

urlpatterns = [
        path('', views.DescriptionsList.as_view(), name= 'descriptions_list'),
        path('<int:pk>/', views.DescriptionDetail.as_view(), name='description_detail'),
        path('<int:pk>/manage', views.description_manage, name='description-manage'),
        path('protocols/', views.ProtocolsList.as_view(), name='protocols_list'),
        path('protocols/create', views.ProtocolCreate.as_view(), name='protocol-create'),
        path('protocols/<int:pk>/', views.ProtocolDetail.as_view(), name = 'protocol_detail'),
        path('protocols/<int:pk>/delete', views.ProtocolDelete.as_view(), name = 'protocol-delete'),
        path('protocols/<int:pk>/update', views.protocol_update, name='protocol-update'),
        path('expression/<int:pk>/update', views.ExpressionUpdate.as_view(), name='expresssion-update'),
]
