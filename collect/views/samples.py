from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.db.models import F, IntegerField, Q, Value
from django.db.models.functions import Cast, Concat
from django.http import HttpResponseBadRequest
from django.shortcuts import get_object_or_404, redirect
from django.template.response import TemplateResponse
from django.urls import reverse, reverse_lazy
from django.utils.timezone import now
from django.views.decorators.http import require_POST
from django.views.generic import DetailView, ListView
from django.views.generic.edit import CreateView, DeleteView
from django_tables2 import RequestConfig

from breadcrumbs.generic import (
    CreateBreadcrumbsMixin,
    DeleteBreadcrumbsMixin,
    DetailBreadcrumbsMixin,
    ListBreadcrumbsMixin,
)
from breadcrumbs.utils import add_plantvariety_breadcrumbs, generate_breadcrumbs
from collect.filters import SeedSampleFilter
from collect.forms import (
    CartSelectForm,
    GerminabilityForm,
    SampleWeightForm,
    SeedSampleForm,
    StorageCreateForm,
    StorageUpdateForm,
)
from collect.models import SeedSample, Storage, StoragePosition
from collect.tables import (
    SeedSampleDuplicatesTable,
    SeedSampleInStorageTable,
    SeedSampleTable,
)
from django_sortable_htmx.views import SortableView
from register.models import PlantVariety, PlantVarietyName


def seedsample_list(request):
    flt = SeedSampleFilter(request.GET)
    queryset = flt.qs.with_latest_weight()

    table = SeedSampleTable(queryset)
    RequestConfig(request, paginate={"per_page": 15}).configure(table)

    context = {"table": table, "filter": flt}

    template_file = "collect/seedsample_list.html"

    if request.headers.get("HX-Request") == "true":
        template_file = "collect/partials/seedsample_table.html"

    context.update(generate_breadcrumbs(request, SeedSample))

    return TemplateResponse(request, template_file, context)


def seedsample_detail(request, pk):
    context = {}
    seedsample = get_object_or_404(SeedSample, pk=pk)
    context["seedsample"] = seedsample
    context["duplicates_table"] = SeedSampleDuplicatesTable(seedsample.duplicate_samples)
    crumbs = generate_breadcrumbs(request, SeedSample, seedsample)
    crumbs = add_plantvariety_breadcrumbs(crumbs, seedsample.variety)
    context.update(crumbs)
    germ_rates = seedsample.germinability_set.annotate(date=F("performed_at")).values("date", "germinability")
    weights = seedsample.sampleweight_set.annotate(date=F("created_at")).values("date", "weight")
    log = list(germ_rates) + list(weights)
    context["log"] = sorted(log, key=lambda e: e["date"], reverse=True)
    return TemplateResponse(request, "collect/seedsample_detail.html", context)


class SeedSampleCreateView(CreateBreadcrumbsMixin, CreateView):
    form_class = SeedSampleForm
    model = SeedSample

    def form_valid(self, form):
        response = super().form_valid(form)
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
        form = super().get_form()
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
            return reverse("collect:seedsample_create")
        return super().get_success_url()


def get_empty_positions_for_accession(instance: SeedSample):
    # TODO: This should be in the model manager
    qs = StoragePosition.objects.all()
    query = Q(seedsample__id=instance.pk)
    query |= Q(seedsample__isnull=True)
    qs = qs.filter(query)
    qs = qs.annotate(
        position_name=Concat("storage__name", Value("-"), "name"),
        posn=Cast("name", output_field=IntegerField()),
    )
    qs = qs.order_by("storage__name", "posn")
    return qs.values("pk", "position_name")


def seedsample_update(request, pk):
    context = {}
    instance = get_object_or_404(SeedSample, pk=pk)
    if request.method == "POST":
        form = SeedSampleForm(request.POST, instance=instance)
        if form.is_valid():
            form.save()
            return redirect(reverse("collect:seedsample_detail", args=(pk,)))
    else:
        form = SeedSampleForm(instance=instance)
    context.update({"form": form, "object": instance})

    context["varieties"] = list(PlantVarietyName.objects.values("variety__id", "name"))
    context["positions"] = list(get_empty_positions_for_accession(instance))
    crumbs = generate_breadcrumbs(request, SeedSample, instance)
    crumbs = add_plantvariety_breadcrumbs(crumbs, instance.variety)
    context.update(crumbs)

    return TemplateResponse(request, "collect/seedsample_update.html", context)


class SeedSampleDeleteView(DeleteBreadcrumbsMixin, DeleteView):
    object: SeedSample
    model = SeedSample
    success_url = reverse_lazy("collect:seedsample_list")


class StorageListView(ListBreadcrumbsMixin, ListView):
    model = Storage
    queryset = Storage.objects.all().order_by("order", "pk")


class StorageDetailView(DetailBreadcrumbsMixin, DetailView):
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
    return TemplateResponse(
        request,
        "collect/storage_detail.html",
        {"storage": storage, "table": table, "sample_count": seed_samples.count()},
    )


class StorageSortView(SortableView):
    model = Storage


def storage_create(request):
    form = StorageCreateForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        with transaction.atomic():
            storage = form.save()
            positions_count = form.cleaned_data["positions"]
            for i in range(positions_count):
                StoragePosition.objects.create(name=f"{i + 1}", storage=storage)
        if "btn-another" in request.POST:
            return redirect(reverse("collect:storage-create"))
        return redirect(reverse("collect:storage_detail", args=[storage.pk]))
    return TemplateResponse(request, "collect/storage_form.html", {"form": form})


def storage_update(request, pk):
    instance = get_object_or_404(Storage, pk=pk)
    if request.method == "POST":
        form = StorageUpdateForm(request.POST, instance=instance)
        if form.is_valid():
            form.save()
            return redirect(reverse("collect:storage_detail", args=(instance.pk,)))
    form = StorageUpdateForm(instance=instance)
    return TemplateResponse(request, "frontpage/_update_form.html", {"form": form})


def storage_delete(request, pk):
    storage = get_object_or_404(Storage, pk=pk)

    if storage.stored_samples:
        return redirect(reverse_lazy("collect:storage_list"))

    if request.POST:
        storage.delete()
        return redirect(reverse_lazy("collect:storage_list"))

    context = {"storage": storage}
    context.update(generate_breadcrumbs(request, Storage, storage))

    return TemplateResponse(request, "collect/storage_confirm_delete.html", context)
