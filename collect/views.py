import csv
from django.db.models.aggregates import Max, Sum
from django.db.models.expressions import Value
from django.db.models.functions import Cast
from django.db.models.functions.text import Concat
from django.db.models import IntegerField, Count
from django.db.models.query_utils import Q
from django.http.response import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.utils.timezone import now
from django.urls.base import reverse, reverse_lazy
from django.views.generic.base import View
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.views.generic.list import ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from calculator.forms import CartItemWeightForm
from collect.forms import GerminabilityForm, SampleWeightForm, SeedSampleForm
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


class SeedSampleListView(ListView):
    model = SeedSample
    paginate_by = 20

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["search"] = self.request.GET.get("search")
        context["view"] = self.request.GET.get("view")
        return context

    def get_queryset(self):
        queryset = SeedSample.objects.all()
        search = self.request.GET.get("search")
        if search:
            if len(search) < 2:
                queryset = queryset.filter(variety__names__name__istartswith=search)
            else:
                queryset = queryset.filter(
                    variety__names__name__unaccent__lower__trigram_similar=search
                )

        if self.request.GET.get("view") == "dupes":
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
        if self.request.GET.get("view") == "stale":
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

        if user.cart_set.count() == 0:
            cart = Cart(user=user)
            cart.save()
        else:
            cart = user.cart_set.last()

        sample = get_object_or_404(SeedSample, pk=self.kwargs["seedsample_id"])
        sample_present = cart.cartitem_set.filter(sample=sample)
        if not sample_present:
            cartitem = CartItem(sample=sample, cart=cart)
            cartitem.save()

        return SeedSampleListView.as_view()(self.request)


@login_required
def change_weight_cartitem(request, cartitem_id):
    if request.user.cart_set.last():
        cartitem = get_object_or_404(CartItem, pk=cartitem_id)
        form = CartItemWeightForm(request.POST, instance=cartitem)
        if form.is_valid():
            form.save()
            return JsonResponse({"data": "ok"})
        else:
            return JsonResponse(form.errors, status=status.HTTP_400_BAD_REQUEST)
    else:
        return JsonResponse({"error": "no cart!"})


class CartItemList(LoginRequiredMixin, ListView):
    model = CartItem
    template_name = "collect/cart.html"
    paginate_by = 20
    cartitem_weight_errors = []

    def get_queryset(self):
        queryset = self.model.objects.filter(cart=self.request.user.cart_set.last()).order_by("sample__position")  # type: ignore
        return queryset

    def post(self, request, *args, **kwargs):
        cart = request.user.cart_set.last()  # type: ignore
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

    def get_context_data(self):
        context = super().get_context_data()
        context["cartitem_weight_errors"] = self.cartitem_weight_errors
        context["cart"] = self.request.user.cart_set.last()
        return context


class CartItemBulkUpdate(View, LoginRequiredMixin):
    def post(self, request, *args, **kwargs):
        cart = request.user.cart_set.last()  # type: ignore
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
    success_url = reverse_lazy("collect:cart-list")


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
        cartitems = self.request.user.cart_set.last().cartitem_set.all()
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
        cart = request.user.cart_set.last()
        for cartitem in cart.cartitem_set.all():
            weight = cartitem.sample.weight - cartitem.weight
            weight_record = SampleWeight(
                seedsample=cartitem.sample, weight=weight, created_at=now().date()
            )
            weight_record.save()
        cart.delete()
        return redirect("collect:seedsample-list")


class CartDeleteSamples(LoginRequiredMixin, View):
    def get(self, request):
        cartitems = self.request.user.cart_set.last().cartitem_set.all()  # type: ignore
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
