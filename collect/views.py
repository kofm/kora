import csv
from typing import Any, Dict
from django import forms
from django.core.paginator import Paginator
from django.db.models.aggregates import Max, Sum
from django.db.models.expressions import Value
from django.db.models.functions import Cast
from django.db.models.functions.text import Concat
from django.db.models import IntegerField, Count
from django.db.models.query import QuerySet
from django.db.models.query_utils import Q
from django.http.response import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.utils.timezone import now
from django.urls.base import reverse, reverse_lazy
from django.views.decorators.http import require_http_methods
from django.views.generic.base import View
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.views.generic.list import ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from calculator.forms import CartItemWeightForm
from collect.forms import (
    GerminabilityForm,
    SampleWeightForm,
    SeedSampleForm,
    SeedSampleYearForm,
)
from django.contrib.auth.decorators import login_required

from collect.models import (
    Cart,
    CartItem,
    Germinability,
    SampleWeight,
    SeedSample,
    Storage,
    StoragePosition,
)
from collect.serializers import (
    GerminabilitySerializer,
    SampleWeightSerializer,
    SeedSampleSerializer,
)
from register.models import PlantVariety, PlantVarietyName


class StorageCreateView(CreateView):
    model = Storage
    fields = [
        "name",
    ]


def seedsample_list_hx(request):
    search = request.GET.get("search")
    page = request.GET.get("page") or 1
    year = request.GET.get("year") or 0
    view = request.GET.get("view")

    queryset = SeedSample.objects.all()

    if search:
        queryset = queryset.filter(
            variety__names__name__unaccent__lower__trigram_similar=search
        )
    if int(year):
        queryset = queryset.filter(growing_season=year)
    if view == "dupes":
        duplicates = (
            SeedSample.objects.all()
            .values("variety_id")
            .annotate(c=Count("id"))
            .order_by("variety")
            .filter(c__gt=1)
        )
        queryset = queryset.filter(
            variety__in=[e["variety_id"] for e in duplicates]
        ).order_by("variety_id", "growing_season")

    # Get samples older than 7 years or weighing less than 200g.
    # The weight is summed across samples of the same variety.
    if view == "stale":
        stale = (
            SeedSample.objects.values("variety")
            .annotate(Max("growing_season"), Sum("sampleweight__weight"))
            .filter(
                Q(growing_season__max__lt=now().year - 7)
                | Q(sampleweight__weight__sum__lt=200)
            )
            .values_list("variety", flat=True)
        )
        queryset = SeedSample.objects.filter(
            variety__in=stale,
        ).order_by("variety_id", "growing_season")

    paginator = Paginator(queryset, 10)
    page_object = paginator.page(page)
    return render(
        request,
        'collect/seedsample_table.html',
        {
            'object_list': page_object,
            'is_paginated': True
        }
    )



class SeedSampleListView(ListView):
    model = SeedSample
    paginate_by = 20

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        context = super().get_context_data(**kwargs)
        year = self.request.GET.get("year")
        context["search"] = self.request.GET.get("search")
        context["view"] = self.request.GET.get("view")
        context["year"] = year
        context["form_year"] = SeedSampleYearForm(initial={"year": year})
        if self.request.user:
            try:
                context["cart"] = Cart.objects.get(user=self.request.user, active=True)
            except:
                pass
        return context

    def get_queryset(self) -> QuerySet[SeedSample]:
        queryset = SeedSample.objects.all()
        search = self.request.GET.get("search")
        view = self.request.GET.get("view")
        year = self.request.GET.get("year")
        if search:
            if len(search) < 2:
                queryset = queryset.filter(variety__names__name__istartswith=search)
            else:
                queryset = queryset.filter(
                    variety__names__name__unaccent__lower__trigram_similar=search
                )

        if view == "dupes":
            duplicates = (
                SeedSample.objects.all()
                .values("variety_id")
                .annotate(c=Count("id"))
                .order_by("variety")
                .filter(c__gt=1)
            )
            queryset = queryset.filter(
                variety__in=[e["variety_id"] for e in duplicates]
            ).order_by("variety_id", "growing_season")

        # Get samples older than 7 years or weighing less than 200g.
        # The weight is summed across samples of the same variety.
        if view == "stale":
            stale = (
                SeedSample.objects.values("variety")
                .annotate(Max("growing_season"), Sum("sampleweight__weight"))
                .filter(
                    Q(growing_season__max__lt=now().year - 7)
                    | Q(sampleweight__weight__sum__lt=200)
                )
                .values_list("variety", flat=True)
            )
            queryset = SeedSample.objects.filter(
                variety__in=stale,
            ).order_by("variety_id", "growing_season")

        if year:
            queryset = queryset.filter(growing_season=year)

        return queryset


class SeedSampleDetailView(DetailView):
    model = SeedSample
    context_object_name = "sample"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["storage_list"] = Storage.objects.filter(
            storageposition__seedsample__isnull=True
        )
        context["variety_list"] = PlantVariety.objects.all()
        context["sample_form"] = SeedSampleForm(instance=self.object)
        context["duplicate_samples"] = SeedSample.objects.filter(
            variety=self.object.variety
        ).exclude(pk=self.object.pk)
        return context


class SeedSampleCreateView(CreateView):
    form_class = SeedSampleForm
    model = SeedSample

    def form_valid(self, form):
        response = super(SeedSampleCreateView, self).form_valid(form)
        weight_form = SampleWeightForm(self.request.POST)
        new_weight = weight_form.save(commit=False)
        new_weight.seedsample = self.object
        new_weight.save()
        if self.request.POST.get("germinability"):
            germinability_form = GerminabilityForm(self.request.POST)
            new_germinability = germinability_form.save(commit=False)
            new_germinability.seedsample = self.object
            new_germinability.save()
        return response

    def get_form(self):
        form = super(SeedSampleCreateView, self).get_form()
        samples_id = SeedSample.objects.all().values_list("sample_id", flat=True)
        sample_id = max(samples_id) + 1 if samples_id else 1
        form.fields["sample_id"].initial = sample_id
        form.fields["growing_season"].initial = now().year - 1
        # form.fields["position"].initial = StoragePosition.objects.filter(
        #     seedsample__isnull=True
        # ).first()
        return form

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["weight_form"] = SampleWeightForm()
        context["germinability_form"] = GerminabilityForm(initial={"after_days": 7})
        context["varieties"] = list(
            PlantVarietyName.objects.values("variety__id", "name")
        )
        context["positions"] = list(
            StoragePosition.objects.filter(seedsample__isnull=True)
            .annotate(
                position_name=Concat("storage__name", Value("-"), "name"),
                posn=Cast("name", output_field=IntegerField()),
            )
            .order_by("storage__name", "posn")
            .values("pk", "position_name")
        )
        return context

    def get_success_url(self):
        if "btn-another" in self.request.POST:
            return reverse("collect:seedsample-create")
        return super().get_success_url()


class SeedSampleUpdateView(UpdateView):
    form_class = SeedSampleForm
    model = SeedSample

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["varieties"] = list(
            PlantVarietyName.objects.values("variety__id", "name")
        )
        context["positions"] = list(
            StoragePosition.objects.filter(
                Q(seedsample__id=self.object.pk) | Q(seedsample__isnull=True)
            )
            .annotate(
                position_name=Concat("storage__name", Value("-"), "name"),
                posn=Cast("name", output_field=IntegerField()),
            )
            .order_by("storage__name", "posn")
            .values("pk", "position_name")
        )
        return context


class SeedSampleDeleteView(DeleteView):
    model = SeedSample
    success_url = reverse_lazy("collect:seedsample-list")


class StorageListView(ListView):
    model = Storage
    paginate_by = 10


class GerminabilityCreateView(CreateView):
    model = Germinability
    fields = ["germinability", "after_days", "performed_at"]

    def get_success_url(self):
        return reverse_lazy("collect:seedsample-detail", args=[self.kwargs["pk"]])

    def form_valid(self, form):
        seedsample = SeedSample.objects.get(pk=self.kwargs["pk"])
        self.object = form.save(commit=False)
        self.object.seedsample = seedsample
        self.object.save()
        return super().form_valid(form)


class GerminabilityDeleteView(DeleteView):
    model = Germinability

    def get_success_url(self):
        return reverse_lazy(
            "collect:seedsample-detail", args=[self.object.seedsample.pk]
        )


class SampleWeightCreateView(CreateView):
    model = SampleWeight
    fields = [
        "weight",
    ]
    template_name = "collect/seedsample_detail.html"

    def get_success_url(self):
        return reverse_lazy("collect:seedsample-detail", args=[self.kwargs["pk"]])

    def form_valid(self, form):
        seedsample = SeedSample.objects.get(pk=self.kwargs["pk"])
        self.object = form.save(commit=False)
        self.object.seedsample = seedsample
        self.object.save()
        return super().form_valid(form)


class SampleWeightDeleteView(DeleteView):
    model = SampleWeight

    def get_success_url(self):
        return reverse_lazy(
            "collect:seedsample-detail", args=[self.object.seedsample.pk]
        )


@api_view(["GET", "POST"])
def germinability(request):
    if request.method == "GET":
        snippets = Germinability.objects.all()
        serializer = GerminabilitySerializer(snippets, many=True)
        return Response(serializer.data)
    if request.method == "POST":
        serializer = GerminabilitySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["GET", "POST"])
def sample_weight(request):
    if request.method == "GET":
        snippets = SampleWeight.objects.all()
        serializer = SampleWeightSerializer(snippets, many=True)
        return Response(serializer.data)
    if request.method == "POST":
        serializer = SampleWeightSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


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


@login_required
def change_weight_cartitem(request, cartitem_id):
    cartitem = get_object_or_404(CartItem, pk=cartitem_id)
    if cartitem.cart.user == request.user:
        form = CartItemWeightForm(request.POST, instance=cartitem)
        if form.is_valid():
            form.save()
            return JsonResponse({"data": "ok"})
        else:
            return JsonResponse(form.errors, status=status.HTTP_400_BAD_REQUEST)


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
    paginator = Paginator(queryset, 5)
    context = {}
    context["cart_id"] = cart_id
    context["cartitems"] = paginator.page(page)
    return render(request, "collect/partials/cart_detail_table.html", context)


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


def sample_labels(request):
    # Create the HttpResponse object with the appropriate CSV header.
    response = HttpResponse(
        content_type="text/csv",
        headers={"Content-Disposition": 'attachment; filename="labels.csv"'},
    )

    n = 84
    empty_positions = (
        StoragePosition.objects.filter(seedsample__isnull=True)
        .annotate(
            position_name=Concat("storage__name", Value("-"), "name"),
            posn=Cast("name", output_field=IntegerField()),
        )
        .order_by("storage__name", "posn")[:n]
    )
    pos = []
    ids = []

    samples_id = SeedSample.objects.all().values_list("sample_id", flat=True)
    sample_id = max(samples_id) + 1 if samples_id else 1

    for x in empty_positions:
        pos.append(x.__str__())

    for x in range(sample_id, sample_id + n):
        ids.append(x)

    writer = csv.writer(response)
    # writer.writerow(["First row", "Foo", "Bar", "Baz"])
    # writer.writerow(["Second row", "A", "B", "C", '"Testing"', "Here's a quote"])
    writer.writerow(["pos", "ids"])
    for x, y in zip(pos, ids):
        writer.writerow([x, y])

    return response


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
