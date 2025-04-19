import json

from django.db import transaction
from django.db.models import CharField, F, IntegerField, Q, Value
from django.db.models.functions import Cast, Concat
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.template.response import TemplateResponse
from django.urls import reverse, reverse_lazy
from django.utils.timezone import now
from django.views.generic import DetailView, ListView
from django.views.generic.edit import CreateView, DeleteView
from django_tables2 import RequestConfig
from render_block import render_block_to_string

from breadcrumbs.generic import (
    CreateBreadcrumbsMixin,
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
from frontpage.views_decorators import htmx_render_block_from_params, htmx_render_blocks
from register.models import PlantVariety, PlantVarietyName


@htmx_render_blocks(["table"])
def sample_list(request):
    flt = SampleFilter(request.GET)
    queryset = flt.qs.with_weight().with_germination()

    table = SampleTable(queryset)
    RequestConfig(request, paginate={"per_page": 15}).configure(table)

    context = {"table": table, "filter": flt}
    context.update(generate_breadcrumbs(request, Sample))

    return TemplateResponse(request, "collect/sample_list.html", context)


@htmx_render_block_from_params()
def sample_detail(request, pk):
    template_name = "collect/sample_detail.html"
    sample = Sample.objects.detail().get(pk=pk)

    context = {
        "sample": sample,
        "log": sample.get_log(),
    }

    duplicates_table = SampleDuplicatesTable(sample.duplicate_samples)
    crumbs = generate_breadcrumbs(request, Sample, sample)
    crumbs = add_plantvariety_breadcrumbs(crumbs, sample.variety)

    context.update(
        {
            "position": f"{sample.position.storage}-{sample.position}",
            "duplicates_table": duplicates_table,
            **crumbs,
        }
    )

    return TemplateResponse(request, template_name, context)


class SampleCreateView(CreateBreadcrumbsMixin, CreateView):
    form_class = SampleForm
    model = Sample

    def form_valid(self, form):
        response = super().form_valid(form)
        weight_form = SampleWeightForm(self.request.POST)
        new_weight = weight_form.save(commit=False)
        new_weight.sample = self.object
        new_weight.save()
        if self.request.POST.get("germinability"):
            germinability_form = GerminabilityForm(self.request.POST)
            new_germinability = germinability_form.save(commit=False)
            new_germinability.sample = self.object
            new_germinability.save()
        return response

    def get_form(self):
        form = super().get_form()
        variety_id = self.request.GET.get("variety_id", None)
        if variety_id:
            variety = get_object_or_404(PlantVariety, pk=variety_id)
            form.fields["variety"].initial = variety
        samples_id = Sample.objects.all().values_list("sample_id", flat=True)
        sample_id = max(samples_id) + 1 if samples_id else 1
        form.fields["sample_id"].initial = sample_id
        form.fields["growing_season"].initial = now().year - 1
        return form

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["weight_form"] = SampleWeightForm()
        germinability_form = GerminabilityForm(initial={"after_days": 7})
        germinability_form.fields["germinability"].required = False
        context["germinability_form"] = germinability_form
        context["varieties"] = list(PlantVarietyName.objects.values("variety__id", "name"))
        context["positions"] = list(
            StoragePosition.objects.filter(sample__isnull=True)
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
            return reverse("collect:sample_create")
        return super().get_success_url()


def get_empty_positions_for_accession(instance: Sample):
    # TODO: This should be in the model manager
    qs = StoragePosition.objects.all()
    query = Q(sample__id=instance.pk)
    query |= Q(sample__isnull=True)
    qs = qs.filter(query)
    qs = qs.annotate(
        position_name=Concat("storage__name", Value("-"), "name"),
        posn=Cast("name", output_field=IntegerField()),
    )
    qs = qs.order_by("storage__name", "posn")
    return qs.values("pk", "position_name")


def sample_update(request, pk):
    context = {}
    instance = get_object_or_404(Sample, pk=pk)
    if request.method == "POST":
        form = SampleForm(request.POST, instance=instance)
        form_weight = SampleWeightForm(request.POST, initial={"weight": instance.weight})
        if form.is_valid() and form_weight.is_valid():
            sample = form.save()
            if form_weight.has_changed():
                sampleweight = sample.last_sampleweight()
                sampleweight.weight = form_weight.cleaned_data.get("weight")
                sampleweight.save()
            return redirect(reverse("collect:sample_detail", args=(pk,)))
    else:
        form = SampleForm(instance=instance)
        form_weight = SampleWeightForm(initial={"weight": instance.weight})

    context.update({"form": form, "form_weight": form_weight, "object": instance})

    context["varieties"] = list(PlantVarietyName.objects.values("variety__id", "name"))
    context["positions"] = list(get_empty_positions_for_accession(instance))

    crumbs = generate_breadcrumbs(request, Sample, instance)
    crumbs = add_plantvariety_breadcrumbs(crumbs, instance.variety)
    context.update(crumbs)

    return TemplateResponse(request, "collect/sample_update.html", context)


class SampleDeleteView(DeleteBreadcrumbsMixin, DeleteView):
    object: Sample
    model = Sample
    success_url = reverse_lazy("collect:sample_list")


class StorageListView(ListBreadcrumbsMixin, ListView):
    model = Storage
    queryset = Storage.objects.all().order_by("order", "pk")


class StorageDetailView(DetailBreadcrumbsMixin, DetailView):
    model = Storage

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        storage_positions = self.object.storageposition_set.all()
        seed_samples = (
            Sample.objects.filter(position__in=storage_positions).select_related("variety").order_by("position")
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
