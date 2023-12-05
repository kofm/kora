from django.urls import path

from . import views

app_name = "collect"

urlpatterns = [
    path("", views.seedsample_list, name="seedsample-list"),
    path("api", views.SeedSampleListAPI.as_view(), name="seedsample-list-api"),
    path("<int:pk>", views.seedsample_detail, name="seedsample-detail"),
    path("new", views.SeedSampleCreateView.as_view(), name="seedsample-create"),
    path("storage", views.StorageListView.as_view(), name="storage-list"),
    path("storage/create", views.storage_create, name="storage-create"),
    path("storage/<int:pk>", views.storage_detail, name="storage-detail"),
    path("storage/<int:pk>/delete", views.storage_delete, name="storage-delete"),
    path("storage/sort", views.StorageSortView.as_view(), name="storage-sort"),
    path("cart/change", views.cart_change_htmx, name="cart-change"),
    path(
        "<int:pk>/update",
        views.SeedSampleUpdateView.as_view(),
        name="seedsample-update",
    ),
    path(
        "<int:pk>/delete",
        views.SeedSampleDeleteView.as_view(),
        name="seedsample-delete",
    ),
    path("cart/change", views.cart_change_htmx, name="cart-change"),
    path("cart/new", views.cart_create, name="cart-create"),
    path("cart/<int:pk>/update", views.cart_update, name="cart-update"),
    path("cart/<int:pk>/delete", views.CartDeleteView.as_view(), name="cart-delete"),
    path("cart/<int:pk>/retrieve", views.cart_retrieve, name="cart-retrieve"),
    path("<int:pk>/cart/add", views.cartitem_add, name="cartitem-add"),
    path("<int:pk>/cart/delete", views.cartitem_delete, name="cartitem-delete"),
    path(
        "cartitem/<int:pk>/setweight",
        views.cartitem_set_weight,
        name="cartitem-setweight",
    ),
]
