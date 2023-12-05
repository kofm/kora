from django_tables2 import RequestConfig
from rest_framework.response import Response
from rest_framework.views import APIView

from collect.filters import SeedSampleFilter
from collect.forms import (
    CartSelectForm,
    GerminabilityForm,
    SampleWeightForm,
    SeedSampleForm,
    StorageCreateForm,
)
from collect.models import SeedSample, Storage, StoragePosition
from collect.serializers import SeedSampleSerializer
from collect.tables import SeedSampleDuplicatesTable, SeedSampleInStorageTable, SeedSampleTable
from django.contrib.auth.decorators import login_required
from django.db.models import IntegerField, Q, Value
from django.db.models.functions import Cast, Concat
from django.http import HttpResponseBadRequest
from django.shortcuts import get_object_or_404, redirect
from django.template.response import TemplateResponse
from django.urls import reverse, reverse_lazy
from django.utils.timezone import now
from django.views.decorators.http import require_POST
from django.views.generic import DetailView, ListView, UpdateView
from django.views.generic.edit import CreateView, DeleteView
from register.models import PlantVariety, PlantVarietyName
from sortable_cards.views import SortableView


def seedsample_list(request):
    context = {}

    filter = SeedSampleFilter(request.GET)
    table = SeedSampleTable(filter.qs)
    RequestConfig(request, paginate={"per_page": 15}).configure(table)
    context.update(
        {
            "table": table,
            "filter": filter,
        }
    )

    if request.user.is_authenticated:
        cart = request.user.carts.active() or None
        context["cart"] = cart
        cart_select_form = CartSelectForm(initial={"cart": cart}, user=request.user)
        context["cart_select_form"] = cart_select_form

    template_file = "collect/seedsample_list.html"

    if request.htmx:
        template_file = "collect/partials/seedsample_table.html"

    return TemplateResponse(request, template_file, context)


@require_POST
@login_required
def cart_change_htmx(request):
    form = CartSelectForm(request.POST, user=request.user)
    if form.is_valid():
        cart = form.save()
        return TemplateResponse(request, "collect/partials/cart_offcanvas.html", {"cart": cart})
    else:
        return HttpResponseBadRequest()


def seedsample_detail(request, pk):
    context = {}
    seedsample = get_object_or_404(SeedSample, pk=pk)
    context["seedsample"] = seedsample
    context["seedsample_duplicates_table"] = SeedSampleDuplicatesTable(seedsample.duplicate_samples)
    return TemplateResponse(request, "collect/seedsample_detail.html", context)


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
        variety_id = self.request.GET.get("variety_id", None)
        if variety_id:
            variety = get_object_or_404(PlantVariety, pk=variety_id)
            form.fields["variety"].initial = variety
        samples_id = SeedSample.objects.all().values_list("sample_id", flat=True)
        sample_id = max(samples_id) + 1 if samples_id else 1
        form.fields["sample_id"].initial = sample_id
        form.fields["growing_season"].initial = now().year - 1
        return form

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["weight_form"] = SampleWeightForm()
        context["germinability_form"] = GerminabilityForm(initial={"after_days": 7})
        context["varieties"] = list(PlantVarietyName.objects.values("variety__id", "name"))
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
        context["varieties"] = list(PlantVarietyName.objects.values("variety__id", "name"))
        context["positions"] = list(
            StoragePosition.objects.filter(Q(seedsample__id=self.object.pk) | Q(seedsample__isnull=True))
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


class SeedSampleListAPI(APIView):
    """
    List all snippets, or create a new snippet.
    """

    def get(self, request, format=None):
        snippets = SeedSample.objects.all()
        serializer = SeedSampleSerializer(snippets, many=True)
        return Response(serializer.data)


class StorageListView(ListView):
    """
    View to display and sort Storage objects
    """

    queryset = Storage.objects.all().order_by("order", "pk")


class StorageDetailView(DetailView):
    model = Storage

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        storage_positions = self.object.storageposition_set.all()
        seed_samples = (
            SeedSample.objects.filter(position__in=storage_positions).select_related("variety").order_by("position")
        )
        table = SeedSampleInStorageTable(seed_samples)
        RequestConfig(self.request, paginate={"per_page": 10}).configure(table)
        context["table"] = table
        return context


def storage_detail(request, pk):
    storage = get_object_or_404(Storage, pk=pk)
    storage_positions = storage.storageposition_set.all()
    seed_samples = (
        SeedSample.objects.filter(position__in=storage_positions).select_related("variety").order_by("position")
    )
    table = SeedSampleInStorageTable(seed_samples)
    RequestConfig(request, paginate={"per_page": 10}).configure(table)
    return TemplateResponse(request, "collect/storage_detail.html", {"storage": storage, "table": table, "sample_count": seed_samples.count()})


class StorageSortView(SortableView):
    """
    Endpoint for sorting Storage objects via htmx
    """

    model = Storage


def storage_create(request):
    """
    View to create a new Storage object
    """

    form = StorageCreateForm()

    if request.POST:
        form = StorageCreateForm(request.POST)
        if form.is_valid():
            storage = form.save()
            positions_count = form.cleaned_data["positions"]
            for i in range(positions_count):
                StoragePosition.objects.create(name=f"{i + 1}", storage=storage)
            if "btn-another" in request.POST:
                return redirect(reverse("collect:storage-create"))
            else:
                return redirect(
                    reverse(
                        "collect:storage-detail",
                        args=[
                            storage.pk,
                        ],
                    )
                )

    return TemplateResponse(request, "collect/storage_form.html", {"form": form})


def storage_delete(request, pk):
    storage = get_object_or_404(Storage, pk=pk)

    if storage.stored_samples:
        return redirect(reverse_lazy("collect:storage-list"))

    if request.POST:
        storage.delete()
        return redirect(reverse_lazy("collect:storage-list"))

    return TemplateResponse(request, "collect/storage_confirm_delete.html", {"storage": storage})
        
