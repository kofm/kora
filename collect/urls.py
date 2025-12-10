from django.urls import path

from . import views

app_name = "collect"

urlpatterns = [
    path("", views.sample_list, name="sample_list"),
    path("<int:pk>", views.sample_detail, name="sample_detail"),
    path("<int:sample_id>/germinability/create", views.germinability_create, name="germinability_create"),
    path("germinability/<int:pk>/update", views.germinability_update, name="germinability_update"),
    path("germinability/<int:pk>/delete", views.germinability_delete, name="germinability_delete"),
    path("<int:sample_id>/sampleweight/create", views.sampleweight_create, name="sampleweight_create"),
    path("sampleweight/<int:pk>/update", views.sampleweight_update, name="sampleweight_update"),
    path("sampleweight/<int:pk>/delete", views.sampleweight_delete, name="sampleweight_delete"),
    path("create", views.sample_create, name="sample_create"),
    path("storage", views.StorageListView.as_view(), name="storage_list"),
    path("storage/create", views.storage_create, name="storage_create"),
    path("storage/<int:pk>", views.StorageDetailView.as_view(), name="storage_detail"),
    path("storage/<int:pk>/update", views.storage_update, name="storage_update"),
    path("storage/<int:pk>/delete", views.storage_delete, name="storage_delete"),
    path("storage/sort", views.StorageSortView.as_view(), name="storage-sort"),
    path("<int:pk>/update", views.sample_update, name="sample_update"),
    path("<int:pk>/delete", views.SampleDeleteView.as_view(), name="sample_delete"),
    path("cart/", views.cart_detail, name="cart_detail"),
    path("cart/activate", views.cart_activate, name="cart_activate"),
    path("cart/create", views.cart_create, name="cart_create"),
    path("cart/<int:pk>/update", views.cart_update, name="cart_update"),
    path("cart/<int:pk>/delete", views.cart_delete, name="cart_delete"),
    path("cart/<int:pk>/retrieve", views.cart_retrieve, name="cart_retrieve"),
    path("cart/<int:pk>/empty", views.cart_empty, name="cart_empty"),
    path("cart/<int:pk>/set_default_weight", views.cart_set_default_weight, name="cart_set_default_weight"),
    path("cartitem/create", views.cartitem_create, name="cartitem_create"),
    path("cartitem/sort/set", views.cartitem_set_sorting, name="cartitem_set_sorting"),
    path("cartitem/<int:pk>/delete", views.cartitem_delete, name="cartitem_delete"),
    path("cartitem/<int:pk>/update", views.cartitem_update, name="cartitem_update"),
    path("cartitem/sort", views.CartItemSortView.as_view(), name="cartitem_sort"),
]
