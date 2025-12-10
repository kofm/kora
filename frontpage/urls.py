from django.urls import path

from . import views

app_name = "frontpage"

urlpatterns = [
    path("", views.index, name="index"),
    path("appearance/set", views.appearance_set, name="appearance_set"),
    path("kora/admin", views.admin, name="admin"),
    path("auth/users/create", views.user_create, name="user_create"),
    path("auth/users/<str:username>/update", views.admin_user_update, name="admin_user_update"),
    path("auth/users/<str:username>/delete", views.user_delete, name="user_delete"),
]


urlpatterns += [
    path("password/change/", views.change_password, name="password_change"),
    path("profile", views.user_detail, name="user_detail"),
    path("profile/update", views.user_update, name="user_update"),
]
