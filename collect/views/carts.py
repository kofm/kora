from django import forms
from django.core.paginator import Paginator
from django.http.response import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls.base import reverse_lazy
from django.views.decorators.http import require_http_methods
from django.views.generic.base import View
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, DeleteView
from django.views.generic.list import ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required

from collect.models import (
    Cart,
    CartItem,
    SampleWeight,
    SeedSample,
)

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


class CartDetailView(DetailView, LoginRequiredMixin):
    model = Cart
    cartitem_weight_errors = []

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
        context["cartitems"] = paginator.page(page)
        return context

@require_http_methods(["GET", ])
def cart_detail_htx(request, cart_id):
    search = request.GET.get("search")
    page = request.GET.get("page") or 1
    queryset = CartItem.objects.filter(cart_id=cart_id)
    if search:
        queryset = queryset.filter(
            sample__variety__names__name__unaccent__lower__trigram_similar=search
        )
    paginator = Paginator(queryset, 15)
    context = {}
    context["cart_id"] = cart_id
    context["cartitems"] = paginator.page(page)
    return render(request, "collect/partials/cart_detail_table.html", context)

@login_required
@require_http_methods(['POST', ])
def cartitem_update_weight_hx(request, pk):
    cartitem = get_object_or_404(CartItem, pk=pk)
    new_weight = request.POST.get("weight")
    if new_weight:
        cartitem.weight = new_weight
        cartitem.save()
    return HttpResponse('')

@login_required
@require_http_methods(['POST',])
def cartitem_update_weight_selected_hx(request):
    # import pdb; pdb.set_trace()
    cartitem_pks = request.POST.getlist("cartitem_pk")
    new_weight = request.POST.get("weight_selected")
    CartItem.objects.filter(pk__in = cartitem_pks).update(weight=new_weight)
    return HttpResponse(new_weight)

        

class CartItemBulkUpdate(View, LoginRequiredMixin):
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


class CartItemDelete(LoginRequiredMixin, DeleteView):
    model = CartItem
    success_url = reverse_lazy("collect:cart-detail")


def samples_export(request):
    if request.method == "GET":
        samples = SeedSample.objects.all()
        serializer = SeedSampleSerializer(samples, many=True)
        return JsonResponse(serializer.data, safe=False)
    else:
        return redirect("collect:seedsample-list")


class CartDelete(LoginRequiredMixin, DeleteView):
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


class CartDeleteSamples(LoginRequiredMixin, View):
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


class CartCreateView(CreateView, LoginRequiredMixin):
    model = Cart
    fields = ["name", "active", "user"]
    success_url = reverse_lazy("collect:seedsample-list")

    def get_form(self):
        form = super().get_form()
        form.fields["user"].widget = forms.HiddenInput()
        form.fields["user"].initial = self.request.user
        return form


class CartListView(ListView, LoginRequiredMixin):
    model = Cart

    def get_queryset(self):
        return Cart.objects.filter(user=self.request.user)


class CartActiveView(View, LoginRequiredMixin):
    def get(self, request, *args, **kwargs):
        active_cart = Cart.objects.get(pk=self.kwargs["pk"], user=self.request.user)
        active_cart.active = True
        active_cart.save()
        return redirect(reverse_lazy("collect:cart-list"))

def cart_create_redirect_htx(request):
    response = HttpResponse()
    response["HX-Redirect"] = reverse_lazy('collect:cart-create')
    return response

def cart_active_hx(request):
    if request.method == "GET":
        cart_id = request.GET.get("cart")
        if cart_id:
            cart = get_object_or_404(Cart, pk=cart_id)
            cart.active = True
            cart.save()
        else:
            cart = None
        return render(request, "collect/seedsample_list_toolbar.html", {"cart": cart})
