from django.urls import path

from . import views

app_name = "frontpage"

urlpatterns = [
    path("", views.index, name="index"),
    path("appearance/set", views.appearance_set, name="appearance_set"),
    path("kora/admin", views.admin, name="admin"),
    path("auth/users/create", views.user_create, name="user_create"),
    path("auth/users/<str:username>/update", views.user_update, name="user_update"),
    path("auth/users/<str:username>/delete", views.user_delete, name="user_delete"),
]
