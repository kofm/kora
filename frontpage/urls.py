from django.urls import path

from . import views

app_name = "frontpage"

urlpatterns = [
    path("", views.index, name="index"),
    path("appearance/set", views.appearance_set, name="appearance_set"),
    path("admin/", views.admin, name="admin"),
    path("admin/users/create", views.user_create, name="user_create"),
    path("admin/users/<str:username>/update", views.admin_user_update, name="admin_user_update"),
    path("admin/users/<str:username>/password/update", views.admin_password_update, name="admin_password_update"),
    path("admin/users/<str:username>/delete", views.user_delete, name="user_delete"),
    path("profile/", views.user_detail, name="user_detail"),
    path("profile/update", views.user_update, name="user_update"),
    path("profile/password/update/", views.password_update, name="password_update"),
]
