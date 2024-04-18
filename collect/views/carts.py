from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.http.response import HttpResponse
from django.shortcuts import get_object_or_404
from django.template.response import TemplateResponse
from django.urls import reverse, reverse_lazy
from django.utils.html import format_html
from django.views.decorators.http import require_GET, require_POST, require_http_methods
from django.views.generic import DeleteView
from collect.forms import CartForm, CartItemNewForm, CartItemSetWeightForm

from collect.models import Cart, CartItem, SampleWeight


@login_required
def cart_create(request):
    context = {}
    form = CartForm()
    if request.POST:
        form = CartForm(request.POST)
        if form.is_valid():
            cart = Cart(name=form.cleaned_data["name"], user=request.user)
            cart.active = True
            cart.save()
            return HttpResponseRedirect(reverse("collect:seedsample-list"))
    context["form"] = form
    return TemplateResponse(request, "collect/cart_form.html", context)


def cart_update(request, pk):
    context = {}
    cart = get_object_or_404(Cart, pk=pk, user=request.user)
    form = CartForm(instance=cart)
    if request.POST:
        form = CartForm(request.POST)
        if form.is_valid():
            cart.name = form.cleaned_data["name"]
            cart.save()
            return HttpResponseRedirect(reverse("collect:seedsample-list"))
    context["form"] = form
    return TemplateResponse(request, "collect/cart_form.html", context)


def cart_retrieve(request, pk):
    context = {}
    cart = get_object_or_404(Cart, pk=pk, user=request.user)
    cartitems = cart.cartitem_set.all()
    if not cartitems.exists():
        return HttpResponseRedirect(reverse("collect:seedsample-list"))
    if request.POST:
        for cartitem in cartitems:
            weight = cartitem.sample.weight - cartitem.weight
            seedsample_weight = SampleWeight(seedsample=cartitem.sample, weight=weight)
            seedsample_weight.save()
        cart.delete()
        return HttpResponseRedirect(reverse("collect:seedsample-list"))
    context["cart"] = cart
    return TemplateResponse(request, "collect/cart_confirm_retrieve.html", context)


class CartDeleteView(DeleteView):
    model = Cart
    success_url = reverse_lazy("collect:seedsample-list")

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(user=self.request.user)


@login_required
@require_POST
def cartitem_add(request, pk):
    weight = request.POST.get("default-weight", None)
    form = CartItemNewForm({"seedsample": pk, "weight": weight}, user=request.user)
    if form.is_valid():
        form.save()
    cart = request.user.carts.active()
    cartitems = sort_cartitems(request, cart.cartitem_set.all())
    return TemplateResponse(
        request,
        "collect/partials/cart_offcanvas.html",
        {"cart": cart, "cartitems": cartitems, "form": form},
    )


def sort_cartitems(request, cartitems):
    CART_SORTING = {
        "variety": "sample__variety__name",
        "growing_season": "sample__growing_season",
        "position": "sample__position",
        "pk": "pk",
    }
    sort_key = request.session.get("cart_sorting", None)
    if sort_key in CART_SORTING:
        sort = CART_SORTING[sort_key]
        cartitems = cartitems.order_by(sort)
    return cartitems


@login_required
@require_GET
def cart_sort(request):
    sort = request.GET.get("sort", None)
    request.session["cart_sorting"] = sort
    cart = request.user.carts.active()
    cartitems = sort_cartitems(request, cart.cartitem_set.all())
    return TemplateResponse(
        request,
        "collect/partials/cart_offcanvas.html",
        {
            "cart": cart,
            "cartitems": cartitems,
        },
    )


@login_required
@require_GET
def cartitem_delete(request, pk):
    cartitem = get_object_or_404(CartItem, pk=pk)
    cartitem.delete()
    return TemplateResponse(
        request,
        "collect/partials/cart_offcanvas.html",
        {"cart": request.user.carts.active()},
    )


@login_required
@require_http_methods(
    [
        "GET",
        "POST",
    ]
)
def cartitem_set_weight(request, pk):
    template = "collect/partials/cartitem_setweight_form.html"
    form = CartItemSetWeightForm(initial={"cartitem": pk})
    if request.POST:
        form = CartItemSetWeightForm(request.POST)
        if form.is_valid():
            cartitem = form.save()
            return HttpResponse(
                format_html(
                    '<span hx-get="{}" hx-trigger="click" hx-swap="outerHTML">{} g</span>',
                    reverse("collect:cartitem-setweight", kwargs={"pk": cartitem.pk}),
                    cartitem.weight,
                )
            )
    cartitem = get_object_or_404(CartItem, pk=pk)
    return TemplateResponse(request, template, {"form": form, "cartitem": cartitem})
