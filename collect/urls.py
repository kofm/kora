from django.urls import path

from . import views

app_name = "collect"

urlpatterns = [
    path("", views.seedsample_list, name="seedsample_list"),
    path("<int:pk>", views.seedsample_detail, name="seedsample-detail"),
    path("new", views.SeedSampleCreateView.as_view(), name="seedsample_create"),
    path("storage", views.StorageListView.as_view(), name="storage_list"),
    path("storage/create", views.storage_create, name="storage-create"),
    path("storage/<int:pk>", views.StorageDetailView.as_view(), name="storage_detail"),
    path("storage/<int:pk>/delete", views.storage_delete, name="storage_delete"),
    path("storage/sort", views.StorageSortView.as_view(), name="storage-sort"),
    path(
        "<int:pk>/update",
        views.SeedSampleUpdateView.as_view(),
        name="seedsample_update",
    ),
    path(
        "<int:pk>/delete",
        views.SeedSampleDeleteView.as_view(),
        name="seedsample_delete",
    ),
    path("cart/change", views.cart_change, name="cart-change"),
    path("cart/new", views.cart_create, name="cart-create"),
    path("cart/<int:pk>/update", views.cart_update, name="cart-update"),
    path("cart/<int:pk>/delete", views.CartDeleteView.as_view(), name="cart-delete"),
    path("cart/<int:pk>/retrieve", views.cart_retrieve, name="cart-retrieve"),
    path("<int:pk>/cart/add", views.cartitem_create, name="cartitem-add"),
    path("cart/sort", views.cart_sort, name="cart-sort"),
    path("<int:pk>/cart/delete", views.cartitem_delete, name="cartitem-delete"),
    path(
        "cartitem/<int:pk>/setweight",
        views.cartitem_set_weight,
        name="cartitem-setweight",
    ),
]
