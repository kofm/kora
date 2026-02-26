from django.contrib import messages
from django.contrib.auth.decorators import permission_required
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.db import transaction
from django.db.models.aggregates import Max
from django.forms import ValidationError
from django.http.response import HttpResponse, HttpResponseBadRequest, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.template.response import TemplateResponse
from django.urls import reverse
from django.views.decorators.http import require_GET, require_POST

from collect.forms import (
    CartCreateForm,
    CartDefaultWeightForm,
    CartItemUpdateForm,
    CartSelectForm,
    CartUpdateForm,
)
from collect.models import Cart, CartItem, CartKind, Sample, SampleWeight
from django_sortable_htmx.views import SortableView
from frontpage.utils.htmx import htmx_response_trigger

CART_SORTING = {
    "variety": "sample__variety__name",
    "growing_season": "sample__growing_season",
    "position": "sample__position",
    "manual": "order",
}


@permission_required("collect.view_cart", raise_exception=True)
def cart_detail(request):
    context = {}
    user = request.user
    cart = Cart.objects.filter(user=user, is_active=True).first()
    if cart:
        items = CartItem.objects.select_related(
            "sample__position__storage",
            "sample__variety__species",
        ).filter(cart_id=cart.pk)
        sorting = request.session.get("cart_sorting", None)
        if sorting:
            items = items.order_by(sorting)
        default_weight_form = CartDefaultWeightForm(instance=cart)
        context.update({"cart": cart, "items": items, "default_weight_form": default_weight_form})
        context["cart_form"] = CartSelectForm(user=user, initial={"cart": cart})
    else:
        context["cart_form"] = CartSelectForm(user=user)
    return TemplateResponse(request, "collect/cart_detail.html", context)


@require_POST
@permission_required("collect.view_cart", raise_exception=True)
def cart_activate(request):
    user = request.user
    form = CartSelectForm(request.POST, user=user)
    if form.is_valid() and "cart" in request.POST:
        form.save()
        return redirect(reverse("collect:cart_detail"))
    return HttpResponseBadRequest()


@permission_required("collect.add_cart", raise_exception=True)
def cart_create(request):
    form = CartCreateForm()
    if request.method == "POST":
        form = CartCreateForm(request.POST)
        if form.is_valid():
            cart = form.save(commit=False)
            cart.is_active = True
            cart.user = request.user
            Cart.objects.filter(user=request.user).deactivate_all()
            cart.save()
            return htmx_response_trigger(["cartUpdated", "closeModal"])
    return render(request, "frontpage/modal_form.html", {"form": form})


@permission_required("collect.change_cart", raise_exception=True)
def cart_update(request, pk):
    instance = get_object_or_404(Cart, pk=pk, user=request.user)
    if request.method == "POST":
        form = CartUpdateForm(request.POST, instance=instance)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.user = request.user
            instance.save()
            return htmx_response_trigger(["cartUpdated", "closeModal"])
    else:
        form = CartUpdateForm(instance=instance)
    return render(request, "frontpage/modal_form.html", {"form": form})


def cart_discard(request, pk):
    instance = get_object_or_404(Cart, pk=pk)
    context = {"cart": instance}
    if request.method == "POST":
        instance.discard()
        return htmx_response_trigger(["cartUpdated", "closeModal", "resultsChanged"])
    return TemplateResponse(request, "frontpage/modal_confirm_delete.html", context)


@permission_required("collect.view_cart", raise_exception=True)
def cart_withdraw(request, pk):
    context = {}
    cart = get_object_or_404(Cart, pk=pk, user=request.user)
    if request.method == "POST":
        cartitems = list(cart.cartitem_set.all())

        sample_ids = [item.sample_id for item in cartitems]
        sample_qs = Sample.objects.with_availability().filter(pk__in=sample_ids).values("pk", "last_weight")
        samples = {sample["pk"]: sample["last_weight"] for sample in sample_qs}
        sampleweights = []
        for item in cartitems:
            sample_id = item.sample_id
            if sample_id not in samples:
                raise ValueError(f"Sample with ID {sample_id} not found in Sample queryset.")

            new_weight = samples[sample_id] - item.weight
            if new_weight < 0:
                messages.error(request, "One of the samples in your cart is not available anymore.")
                return HttpResponse()

            sampleweight = SampleWeight(sample_id=sample_id, weight=new_weight)
            sampleweights.append(sampleweight)

        SampleWeight.objects.bulk_create(sampleweights)
        cart.delete()
        return htmx_response_trigger(["cartUpdated", "closeModal", "resultsChanged"])

    context = {"cart": cart}
    return render(request, "collect/cart_confirm_withdraw.html", context)


@permission_required("collect.change_cart", raise_exception=True)
def cart_empty(request, pk):
    cart = get_object_or_404(Cart, pk=pk)
    context = {"cart": cart}
    if request.method == "POST":
        cart.cartitem_set.all().delete()
        return htmx_response_trigger(["cartUpdated"])
    return render(request, "collect/cart_empty.html", context)


@permission_required("collect.delete_cart", raise_exception=True)
def cart_delete(request, pk):
    cart = get_object_or_404(Cart, pk=pk)
    if request.method == "POST":
        cart.delete()
        return htmx_response_trigger(["cartUpdated", "closeModal", "resultsChanged"])
    return render(request, "collect/cart_confirm_delete.html", {"cart": cart})


@permission_required("collect.view_cart", raise_exception=True)
@require_POST
def cart_set_default_weight(request, pk):
    instance = get_object_or_404(Cart, pk=pk)
    form = CartDefaultWeightForm(request.POST, instance=instance)
    if form.is_valid():
        instance.default_weight = form.cleaned_data["default_weight"]
        instance.save()
        return HttpResponse()
    else:
        return HttpResponseBadRequest()


@permission_required("collect.add_cartitem", raise_exception=True)
@require_POST
def cartitem_create(request):
    try:
        cart = Cart.objects.get(user=request.user, is_active=True)
    except Cart.DoesNotExist:
        cart = None

    sample_id = request.POST.get("sample_id", None)

    if not sample_id:
        return JsonResponse({"error": "Invalid input."}, status=409)

    if not cart:
        messages.error(request, "No cart selected.")
        return HttpResponse(headers={"HX-Reswap": "none"})

    try:
        with transaction.atomic():
            order_max = CartItem.objects.filter(cart=cart).aggregate(Max("order"))["order__max"] or 0
            defaults = {"order": order_max + 1}
            if cart.kind == CartKind.WITHDRAWAL:
                defaults["weight"] = cart.default_weight

            cartitem, created = CartItem.objects.get_or_create(
                sample_id=sample_id,
                cart=cart,
                defaults=defaults,
            )

            if not created:
                if cart.kind == CartKind.WITHDRAWAL:
                    messages.warning(request, f"{cartitem.weight:g} g of this sample are already in your cart.")
                else:
                    messages.warning(request, "This sample is already in your disposal cart.")
                return HttpResponse(headers={"HX-Reswap": "none"})

            if cart.kind == CartKind.WITHDRAWAL:
                message = f"{cart.default_weight} g added to {cart.name}."
            else:
                message = f"Sample added to {cart.name} for disposal."
            cartitem.save()
            messages.success(request, message)

            return htmx_response_trigger(["cartUpdated", "logItemUpdated", "resultsChanged"])

    except ValidationError as e:
        for msg in e.messages:
            messages.error(request, msg)

    return redirect(reverse("collect:cart_detail"))


@permission_required("collect.change_cartitem", raise_exception=True)
@require_GET
def cartitem_set_sorting(request):
    sort_key = request.GET.get("sort", None)
    if sort_key in CART_SORTING:
        request.session["cart_sorting"] = CART_SORTING[sort_key]
    return redirect(reverse("collect:cart_detail"))


@permission_required("collect.delete_cartitem", raise_exception=True)
@require_GET
def cartitem_delete(request, pk):
    cartitem = get_object_or_404(CartItem, pk=pk)
    if request.user.pk == cartitem.cart.user_id:
        cartitem.delete()
        return htmx_response_trigger(["cartUpdated", "logItemUpdated", "resultsChanged"])


@permission_required("collect.change_cartitem", raise_exception=True)
def cartitem_update(request, pk):
    cartitem = get_object_or_404(CartItem, pk=pk)
    form = CartItemUpdateForm(instance=cartitem)
    if request.method == "POST":
        form = CartItemUpdateForm(request.POST, instance=cartitem)
        if form.is_valid():
            form.save()
            return htmx_response_trigger(["cartUpdated", "logItemUpdated", "closeModal", "resultsChanged"])
    return TemplateResponse(request, "collect/partials/cartitem_update.html", {"form": form})


class CartItemSortView(PermissionRequiredMixin, SortableView):
    model = CartItem
    permission_required = ["collect.change_cartitem"]

    def post(self, request):
        request.session["cart_sorting"] = CART_SORTING["manual"]
        return super().post(request)
