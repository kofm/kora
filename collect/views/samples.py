import json
from typing import override

from django.db import transaction
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.template.response import TemplateResponse
from django.urls import reverse, reverse_lazy
from django.views.generic import DetailView, ListView
from django.views.generic.edit import DeleteView
from django_tables2 import RequestConfig

from breadcrumbs.generic import (
    DeleteBreadcrumbsMixin,
    DetailBreadcrumbsMixin,
    ListBreadcrumbsMixin,
)
from breadcrumbs.utils import add_plantvariety_breadcrumbs, generate_breadcrumbs
from collect.filters import SampleFilter
from collect.forms import (
    GerminabilityForm,
    SampleForm,
    SampleWeightForm,
    StorageCreateForm,
    StorageUpdateForm,
)
from collect.models import Germinability, Sample, SampleWeight, Storage, StoragePosition
from collect.tables import (
    SampleDuplicatesTable,
    SampleInStorageTable,
    SampleTable,
)
from django_sortable_htmx.views import SortableView
from frontpage.views_decorators import htmx_render_blocks


@htmx_render_blocks(["table"])
def sample_list(request):
    flt = SampleFilter(request.GET)
    queryset = flt.qs.with_availability().with_germination()

    table = SampleTable(queryset)
    RequestConfig(request, paginate={"per_page": 15}).configure(table)

    context = {"table": table, "filter": flt}
    context.update(generate_breadcrumbs(request, Sample))

    return TemplateResponse(request, "collect/sample_list.html", context)


@htmx_render_blocks(["log", "weight", "germinability"])
def sample_detail(request, pk):
    template_name = "collect/sample_detail.html"
    sample = Sample.objects.detail().with_availability().get(pk=pk)

    duplicates_table = SampleDuplicatesTable(sample.duplicate_samples)
    crumbs = generate_breadcrumbs(request, Sample, sample)
    crumbs = add_plantvariety_breadcrumbs(crumbs, sample.variety)

    context = {"sample": sample, "log": sample.get_log(), "duplicates_table": duplicates_table, **crumbs}

    return TemplateResponse(request, template_name, context)


def sample_create(request):
    if request.method == "POST":
        form = SampleForm(request.POST)
        form_weight = SampleWeightForm(request.POST)
        if form.is_valid() and form_weight.is_valid():
            with transaction.atomic():
                sample = form.save()
                weight = form_weight.save(commit=False)
                weight.sample = sample
                weight.save()
            if "another" in request.POST:
                return redirect(reverse("collect:sample_create"))
            return redirect(reverse("collect:sample_list"))
    else:
        form = SampleForm()
        form_weight = SampleWeightForm()
    return TemplateResponse(
        request,
        "collect/sample_create.html",
        {"form": form, "form_weight": form_weight, **generate_breadcrumbs(request, Sample), "model_name": "Sample"},
    )


def sample_update(request, pk):
    context = {}
    sample = get_object_or_404(Sample, pk=pk)
    if request.method == "POST":
        form = SampleForm(request.POST, instance=sample)
        if form.is_valid():
            sample = form.save()
            return redirect(reverse("collect:sample_detail", args=(pk,)))
    else:
        form = SampleForm(instance=sample)

    context.update({"form": form, "object": sample})

    crumbs = generate_breadcrumbs(request, Sample, sample)
    crumbs = add_plantvariety_breadcrumbs(crumbs, sample.variety)
    context.update(crumbs)

    return TemplateResponse(request, "collect/sample_update.html", context)


class SampleDeleteView(DeleteBreadcrumbsMixin, DeleteView):
    object: Sample
    model = Sample
    success_url = reverse_lazy("collect:sample_list")


class StorageListView(ListBreadcrumbsMixin, ListView):
    model = Storage
    queryset = Storage.objects.prefetch_related("storageposition_set").with_position_counts().order_by("order", "pk")


class StorageDetailView(DetailBreadcrumbsMixin, DetailView):
    model = Storage

    def get_queryset(self):
        return Storage.objects.with_position_counts()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        storage_positions = self.object.storageposition_set.all()
        seed_samples = (
            Sample.objects.with_availability()
            .filter(position__in=storage_positions)
            .select_related("variety")
            .order_by("position")
        )
        table = SampleInStorageTable(seed_samples)
        RequestConfig(self.request, paginate={"per_page": 10}).configure(table)
        context["table"] = table
        return context


def storage_detail(request, pk):
    storage = get_object_or_404(Storage, pk=pk)
    storage_positions = storage.storageposition_set.all()
    seed_samples = Sample.objects.filter(position__in=storage_positions).select_related("variety").order_by("position")
    table = SampleInStorageTable(seed_samples)
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


def sampleweight_create(request, sample_id):
    if request.method == "POST":
        form = SampleWeightForm(request.POST)
        if form.is_valid():
            sampleweight = form.save(commit=False)
            sampleweight.sample_id = sample_id
            sampleweight.save()
            return HttpResponse(headers={"Hx-Trigger": json.dumps({"closeModal": True, "logItemUpdated": True})})
    else:
        form = SampleWeightForm()
    return TemplateResponse(
        request,
        "collect/partials/sampleweight_create.html",
        {"form": form},
    )


def sampleweight_update(request, pk):
    sampleweight = get_object_or_404(SampleWeight, pk=pk)
    if request.method == "POST":
        form = SampleWeightForm(request.POST, instance=sampleweight)
        if form.is_valid():
            form.save()
            return HttpResponse(headers={"Hx-Trigger": json.dumps({"closeModal": True, "logItemUpdated": True})})
    else:
        form = SampleWeightForm(instance=sampleweight)
    return render(
        request,
        "collect/partials/sampleweight_update.html",
        {"sampleweight": sampleweight, "form": form},
    )


def sampleweight_delete(request, pk):
    sampleweight = get_object_or_404(SampleWeight, pk=pk)
    if request.method == "POST":
        sampleweight.delete()
        return HttpResponse(headers={"Hx-Trigger": json.dumps({"closeModal": True, "logItemUpdated": True})})
    return render(
        request,
        "collect/partials/sampleweight_confirm_delete.html",
        {},
    )


def germinability_create(request, sample_id):
    if request.method == "POST":
        form = GerminabilityForm(request.POST)
        if form.is_valid():
            germinability = form.save(commit=False)
            germinability.sample_id = sample_id
            germinability.save()
            return HttpResponse(headers={"Hx-Trigger": json.dumps({"closeModal": True, "logItemUpdated": True})})
    else:
        form = GerminabilityForm()
    return TemplateResponse(
        request,
        "collect/partials/germinability_create.html",
        {"form": form},
    )


def germinability_update(request, pk):
    germinability = get_object_or_404(Germinability, pk=pk)
    if request.method == "POST":
        form = GerminabilityForm(request.POST, instance=germinability)
        if form.is_valid():
            form.save()
            return HttpResponse(headers={"Hx-Trigger": json.dumps({"closeModal": True, "logItemUpdated": True})})
    else:
        form = GerminabilityForm(instance=germinability)
    return TemplateResponse(
        request,
        "collect/partials/germinability_update.html",
        {"germinability": germinability, "form": form},
    )


def germinability_delete(request, pk):
    germinability = get_object_or_404(Germinability, pk=pk)
    if request.method == "POST":
        germinability.delete()
        return HttpResponse(headers={"Hx-Trigger": json.dumps({"closeModal": True, "logItemUpdated": True})})
    return render(
        request,
        "collect/partials/germinability_confirm_delete.html",
        {},
    )
