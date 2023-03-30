from django.contrib.auth.decorators import login_required
from django.http.response import HttpResponse
from django.shortcuts import get_object_or_404
from django.template.response import TemplateResponse
from django.urls import reverse
from django.utils.html import format_html
from django.views.decorators.http import require_GET, require_POST, require_http_methods
from collect.forms import CartItemNewForm, CartItemSetWeightForm

from collect.models import CartItem


@login_required
@require_POST
def cartitem_add(request, pk):
    weight = request.POST.get("default-weight", None)
    form = CartItemNewForm({"seedsample": pk, "weight": weight}, user=request.user)
    if form.is_valid():
        form.save()
    return TemplateResponse(
        request,
        "collect/partials/cart_offcanvas.html",
        {"cart": request.user.carts.active(), "form": form},
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
