from django.urls import path

from . import views

app_name = "collect"

urlpatterns = [
    path("", views.SeedSampleListView.as_view(), name="seedsample-list"),
    path("_hx", views.seedsample_list_hx, name="seedsample-list-hx"),
    path("sample/labels", views.sample_labels, name="seedsample-labels"),
    path("sample/<int:pk>", views.SeedSampleDetailView.as_view(), name="seedsample-detail"),
    path("sample/<int:pk>/update", views.SeedSampleUpdateView.as_view(), name="seedsample-update"),
    path("sample/create", views.SeedSampleCreateView.as_view(), name="seedsample-create"),
    path("sample/<int:pk>/delete", views.SeedSampleDeleteView.as_view(), name="seedsample-delete"),
    path("storage/create", views.StorageCreateView.as_view(), name="storage-create"),
    path("storage", views.StorageListView.as_view(), name="storage-list"),
    path("germinability", views.germinability, name="germinability"),
    path("sample/<int:pk>/germinability/create", views.GerminabilityCreateView.as_view(), name="germinability-create"),
    path("sample/<int:pk>/sampleweight/create", views.SampleWeightCreateView.as_view(), name="sampleweight-create"),
    path("germinability/<int:pk>/delete", views.GerminabilityDeleteView.as_view(), name="germinability-delete"),
    path("sampleweight", views.sample_weight, name="sample-weight"),
    path("sampleweight/<int:pk>/delete", views.SampleWeightDeleteView.as_view(), name="sampleweight-delete"),
    path("cart/add/<int:seedsample_id>", views.CartItemAdd.as_view(), name="cart-add"),
    path("cart/<int:pk>", views.CartDetailView.as_view(), name="cart-detail"),
    path("cart/htx/<int:cart_id>", views.cart_detail_htx, name="cart-detail-htx"),
    path("cart/retrieve", views.CartRetrieve.as_view(), name="cart-retrieve"),
    path("cart/trash", views.CartDeleteSamples.as_view(), name="cart-delete-samples"),
    path("cart/<int:pk>/delete", views.CartDelete.as_view(), name="cart-delete"),
    path("cartitem/<int:pk>/weight/update", views.cartitem_update_weight_hx, name="cartitem-weight-update-hx"),
    path("cartitems/weight/update", views.cartitem_update_weight_selected_hx, name="cartitem-weight-update-selected-hx"),
    path("cartitem/<int:pk>/delete", views.CartItemDelete.as_view(), name="cartitem-delete"),
    path("export", views.samples_export, name="samples-export"),
    path("cart/labels", views.cartitem_labels, name="cartitem-labels"),
    path("carts/", views.CartListView.as_view(), name="cart-list"),
    path("cart/<int:pk>/favourite", views.CartActiveView.as_view(), name="cart-favourite"),
    path("cart/favourite", views.cart_active_hx, name="cart-fav"),
    path("cart/create", views.CartCreateView.as_view(), name="cart-create"),
    path("cart/htx/create", views.cart_create_redirect_htx, name="cart-create-htx"),
]
