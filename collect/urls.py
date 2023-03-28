from django.urls import path

from . import views

app_name = "collect"

urlpatterns = [
    path("", views.seedsample_list, name="seedsample-list"),
    path("sample/<int:pk>", views.SeedSampleDetailView.as_view(), name="seedsample-detail"),
    path("sample/create", views.SeedSampleCreateView.as_view(), name="seedsample-create"),
    path("sample/<int:pk>/update", views.SeedSampleUpdateView.as_view(), name="seedsample-update"),
    path("sample/<int:pk>/delete", views.SeedSampleDeleteView.as_view(), name="seedsample-delete"),
    path("sample/labels", views.sample_labels, name="seedsample-labels"),

    path("sampleweight/<int:pk>/delete", views.SeedSampleDetailView.as_view(), name="sampleweight-delete"),
    path("sampleweight/<int:pk>/create", views.sampleweight_create_hx, name="sampleweight-create"),

    path("germinability/<int:pk>/delete", views.SeedSampleDetailView.as_view(), name="germinability-delete"),
    path("germinability/<int:pk>/create", views.SeedSampleDetailView.as_view(), name="germinability-create"),

    path("cart/create", views.CartCreateView.as_view(), name="cart-create"),
    path("cart/<int:pk>/", views.CartDetailView.as_view(), name="cart-detail"),
    path("cart/<int:pk>/delete", views.CartDeleteView.as_view(), name="cart-delete"),
    path("cart/<int:pk>/labels", views.cartitem_labels, name="cart-labels"),
    path("cart/retrieve", views.CartRetrieve.as_view(), name="cart-retrieve"),

    path("cartitem/update", views.cartitem_update_weight_selected_hx, name="cartitem-update-hx"),
    path("cartitem/sel/update", views.cartitem_update_weight_selected_hx, name="cartitem-update-sel-hx"),
    path("cartitem/<int:pk>/update", views.cartitem_update_weight_hx, name="cartitem-update-hx"),
    path("cart/<int:pk>/hx", views.cart_detail_hx, name="cart-detail-hx"),
    path("cartitem/<int:pk>/delete", views.CartItemDelete.as_view(), name="cartitem-delete"),
    path("cartitem/<int:seedsample_id>/add", views.CartItemAdd.as_view(), name="cartitem-add"),
]
