from django.urls import path

from . import views

app_name = "collect"

urlpatterns = [
    path("", views.seedsample_list, name="seedsample-list"),
    path("<int:pk>", views.seedsample_detail, name="seedsample-detail"),
    path("new", views.SeedSampleCreateView.as_view(), name="seedsample-create"),
    path("cart/change", views.cart_change_htmx, name="cart-change"),
    path("<int:pk>/cart/add", views.cartitem_add, name="cartitem-add"),
    path("<int:pk>/cart/delete", views.cartitem_delete, name="cartitem-delete"),
    path("cartitem/<int:pk>/setweight", views.cartitem_set_weight, name="cartitem-setweight"),
]
