import csv
from typing import Any, List
from django import forms
from django.core.exceptions import PermissionDenied
from django.core.paginator import Paginator
from django.http import HttpRequest
from django.http.response import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls.base import reverse_lazy
from django.views.decorators.http import require_GET, require_POST, require_http_methods
from django.views.generic.base import View
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, DeleteView
from django.views.generic.list import ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from collect.forms import CartSelectForm

from collect.models import (
    Cart,
    CartItem,
    SampleWeight,
    SeedSample,
)
from collect.serializers import SeedSampleSerializer
from collect.views.samples import SeedSampleListView


class OwnerRequiredMixin:
    def dispatch(self, request, *args, **kwargs):
        obj = self.get_object()
        if obj.user != request.user:
            raise PermissionDenied
        return super().dispatch(request, *args, **kwargs)


class CartDetailView(LoginRequiredMixin, OwnerRequiredMixin, DetailView):
    model = Cart
    cartitem_weight_errors: List[str] = []

    def post(self, request, *args, **kwargs):
        cart = Cart.objects.get(user=self.request.user, active=True)
        weight = float(request.POST.get("weight"))  # type: ignore
        if cart and weight:
            self.cartitem_weight_errors = []
            cartitems = cart.cartitem_set.all()
            for cartitem in cartitems:
                sample_weight = cartitem.sample.weight
                if weight <= sample_weight:
                    cartitem.weight = weight
                else:
                    cartitem.weight = sample_weight
                    error = (
                        cartitem.sample.variety.name + ": " + str(sample_weight) + " g"
                    )
                    self.cartitem_weight_errors.append(error)
                cartitem.save()
        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["cartitem_weight_errors"] = self.cartitem_weight_errors
        cartitems = self.object.cartitem_set.all()
        paginator = Paginator(cartitems, 15)
        page = self.request.GET.get("page") or 1
        context["cart_select_form"] = CartSelectForm(user=self.request.user)
        context["cartitems"] = paginator.page(page)
        return context


@require_GET
def cart_detail_hx(request, pk):
    search = request.GET.get("search")
    page = request.GET.get("page") or 1
    queryset = CartItem.objects.filter(cart_id=pk)
    if search:
        queryset = queryset.filter(
            sample__variety__names__name__unaccent__lower__trigram_similar=search
        )
    paginator = Paginator(queryset, 15)
    context = {}
    context["cart_id"] = pk
    context["cartitems"] = paginator.page(page)
    return render(request, "collect/partials/cart_detail_table.html", context)


class CartCreateView(LoginRequiredMixin, CreateView):
    model = Cart
    fields = ["name", "active", "user"]
    success_url = reverse_lazy("collect:seedsample-list")

    def get_form(self):
        form = super().get_form()
        form.fields["user"].widget = forms.HiddenInput()
        form.fields["user"].initial = self.request.user
        return form


class CartDeleteView(LoginRequiredMixin, OwnerRequiredMixin, DeleteView):
    model = Cart
    success_url = reverse_lazy("collect:seedsample-list")


class CartRetrieve(LoginRequiredMixin, View):
    def get(self, request):
        cartitems = CartItem.objects.filter(
            cart__user=self.request.user, cart__active=True
        )
        return render(
            request,
            "collect/cart_confirm_retrieve.html",
            {
                "cartitems": cartitems,
                "message_action": "<b>retrieve your cart</b>",
                "message_info": "After confirmation, these quantities will be subtracted from the samples and the weights will be updated accordingly",
            },
        )

    def post(self, request):
        cart = request.user.carts.get(active=True)

        for cartitem in cart.cartitem_set.all():
            new_weight = cartitem.sample.weight - cartitem.weight
            weight_updated = SampleWeight(seedsample=cartitem.sample, weight=new_weight)
            weight_updated.save()

        return redirect("collect:seedsample-list")


class CartItemAdd(LoginRequiredMixin, View):
    def get(self, *args, **kwargs):
        user = self.request.user
        cart = get_object_or_404(Cart, user=user, active=True)
        sample = get_object_or_404(SeedSample, pk=self.kwargs["seedsample_id"])
        sample_present = cart.cartitem_set.filter(sample=sample)
        if not sample_present:
            cartitem = CartItem(sample=sample, cart=cart)
            cartitem.save()
        return SeedSampleListView.as_view()(self.request)


class CartItemDelete(LoginRequiredMixin, DeleteView):
    model = CartItem
    success_url = reverse_lazy("collect:cart-detail")


@login_required
@require_POST
def cartitem_update_weight_hx(request, pk):
    cartitem = get_object_or_404(CartItem, pk=pk)
    new_weight = request.POST.get("weight")
    if new_weight:
        cartitem.weight = new_weight
        cartitem.save()
    return HttpResponse("")


@login_required
@require_POST
def cartitem_update_weight_selected_hx(request):
    # import pdb; pdb.set_trace()
    cartitem_pks = request.POST.getlist("cartitem_pk")
    new_weight = request.POST.get("weight_selected")
    CartItem.objects.filter(pk__in=cartitem_pks).update(weight=new_weight)
    return HttpResponse(new_weight)


class CartItemBulkUpdate(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        cart = self.request.user.carts.get(active=True)
        weight = float(request.POST.get("weight"))  # type: ignore
        if cart and weight:
            self.cartitem_weight_errors = []
            cartitems = cart.cartitem_set.all()
            for cartitem in cartitems:
                sample_weight = cartitem.sample.weight
                if weight <= sample_weight:
                    cartitem.weight = weight
                else:
                    cartitem.weight = sample_weight
                    error = (
                        cartitem.sample.variety.name + ": " + str(sample_weight) + " g"
                    )
                    self.cartitem_weight_errors.append(error)
                cartitem.save()


class CartItemBulkDelete(LoginRequiredMixin, View):
    def get(self, request):
        cartitems = CartItem.objects.filter(
            cart__user=self.request.user, cart__active=True
        )
        return render(
            request,
            "collect/cart_confirm_retrieve.html",
            {
                "cartitems": cartitems,
                "message_action": "<b>delete all the samples</b> present in your cart from the reference collection",
                "message_info": "After confirmation, the samples will be removed from your collection and cannot be undone",
            },
        )


def cartitem_labels(request):
    # Create the HttpResponse object with the appropriate CSV header.
    response = HttpResponse(
        content_type="text/csv",
        headers={"Content-Disposition": 'attachment; filename="labels.csv"'},
    )

    cart = request.user.cart_set.last()
    print(cart)

    writer = csv.writer(response)
    writer.writerow(["variety", "id", "position"])
    for cartitem in cart.cartitem_set.all():
        writer.writerow(
            [
                cartitem.sample.variety,
                cartitem.sample.sample_id,
                cartitem.sample.position,
            ]
        )

    return response
