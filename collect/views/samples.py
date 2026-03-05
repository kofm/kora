from django.contrib.auth.decorators import permission_required
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.db import transaction
from django.http import Http404
from django.shortcuts import get_object_or_404, redirect, render
from django.template.response import TemplateResponse
from django.urls import reverse, reverse_lazy
from django.views.generic import DetailView, ListView
from django_tables2 import RequestConfig

from breadcrumbs.generic import (
    DetailBreadcrumbsMixin,
    ListBreadcrumbsMixin,
)
from breadcrumbs.utils import add_plantvariety_breadcrumbs, breadcrumbs_context, generate_breadcrumbs, list_breadcrumb
from collect.filters import SampleFilter
from collect.forms import (
    GerminabilityForm,
    SampleForm,
    SampleRestoreForm,
    SampleWeightForm,
    StorageCreateForm,
    StorageUpdateForm,
)
from collect.models import Germinability, Sample, SampleStatus, SampleWeight, Storage, StoragePosition
from collect.tables import (
    DiscardedSampleTable,
    DuplicatedSampleTable,
    SampleInStorageTable,
    SampleTable,
)
from django_sortable_htmx.views import SortableView
from frontpage.templatetags.components import get_action_url_from_instance, get_permission_from_instance
from frontpage.utils.htmx import htmx_response_trigger, htmx_response_trigger_close_modal
from frontpage.views_decorators import htmx_render_blocks


@htmx_render_blocks(["main"])
@permission_required("collect.view_sample")
def sample_list(request):
    flt = SampleFilter(request.GET, queryset=Sample.objects.all())
    queryset = flt.qs.with_availability().with_germination()

    discarded_flt = SampleFilter(request.GET, queryset=Sample.all_objects.discarded())
    discarded_count = discarded_flt.qs.count()

    table = SampleTable(queryset)
    RequestConfig(request, paginate={"per_page": 15}).configure(table)

    context = {
        "table": table,
        "filter": flt,
        "discarded_count": discarded_count,
    }
    context.update(generate_breadcrumbs(request, Sample))

    return TemplateResponse(request, "collect/sample_list.html", context)


@htmx_render_blocks(["main"])
@permission_required("collect.view_sample")
def discarded_sample_list(request):
    flt = SampleFilter(request.GET, queryset=Sample.all_objects.discarded())
    queryset = flt.qs.with_availability().with_germination()

    table = DiscardedSampleTable(queryset)
    RequestConfig(request, paginate={"per_page": 15}).configure(table)

    header = {
        "page_title": "Discarded Samples",
        "subtitle": "Samples removed from collection",
        "create_url": None,
    }
    context = {
        "table": table,
        "filter": flt,
        "header": header,
    }
    breadcrumbs = [list_breadcrumb(Sample), ("Discarded", "")]
    context.update(breadcrumbs_context(breadcrumbs))

    return TemplateResponse(request, "collect/discarded_sample_list.html", context)


@permission_required("collect.delete_sample", raise_exception=True)
def discarded_sample_bulk_delete(request):
    if request.method == "POST":
        flt = SampleFilter(request.POST, queryset=Sample.all_objects.discarded())
        flt.qs.delete()
        return htmx_response_trigger(["resultsChanged"])
    return TemplateResponse(request, "collect/discarded_sample_confirm_bulk_delete.html", {})


@permission_required("collect.delete_sample", raise_exception=True)
def discarded_sample_delete(request, pk):
    instance = Sample.all_objects.get(pk=pk)
    if request.method == "POST":
        instance.delete()
        return htmx_response_trigger(["closeModal", "resultsChanged"])
    context = {"instance": instance}
    return TemplateResponse(request, "frontpage/modal_confirm_delete.html", context)


@permission_required("collect.change_sample", raise_exception=True)
def discarded_sample_restore(request, pk):
    instance = get_object_or_404(Sample.all_objects, pk=pk)

    if instance.status != SampleStatus.DISCARDED:
        raise Http404()

    if request.method == "POST":
        form = SampleRestoreForm(request.POST, instance=instance)
        if form.is_valid():
            position = form.cleaned_data["position"]
            instance.restore(position=position)
            return htmx_response_trigger(["closeModal", "resultsChanged"])
    else:
        form = SampleRestoreForm(instance=instance)

    return TemplateResponse(request, "frontpage/modal_form.html", {"form": form})


@htmx_render_blocks(["log", "weight", "germinability"])
@permission_required("collect.view_sample")
def sample_detail(request, pk):
    sample = Sample.objects.detail().with_availability().get(pk=pk)

    log = []

    for entry in sample.get_log():
        instance = entry["instance"]
        urls = {}
        for action, perm in (("update", "change"), ("delete", "delete")):
            permission = get_permission_from_instance(perm, instance)
            user_is_allowed = request.user.has_perm(permission)
            urls[action] = get_action_url_from_instance(action, instance) if user_is_allowed else None

        log.append(
            {
                "date": entry["date"],
                "value": str(instance),
                "update_url": urls["update"],
                "delete_url": urls["delete"],
            }
        )

    duplicates_table = DuplicatedSampleTable(sample.duplicate_samples)
    crumbs = generate_breadcrumbs(request, Sample, sample)
    crumbs = add_plantvariety_breadcrumbs(crumbs, sample.variety)

    context = {"sample": sample, "log": log, "duplicates_table": duplicates_table, **crumbs}

    return TemplateResponse(request, "collect/sample_detail.html", context)


@permission_required("collect.add_sample", raise_exception=True)
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


@permission_required("collect.change_sample", raise_exception=True)
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


def sample_delete(request, pk):
    instance = get_object_or_404(Sample, pk=pk)
    if request.method == "POST":
        instance.discard()
        return redirect(reverse("collect:sample_list"))
    context = {"instance": instance}
    return TemplateResponse(request, "collect/sample_confirm_delete.html", context)


class StorageListView(PermissionRequiredMixin, ListBreadcrumbsMixin, ListView):
    model = Storage
    queryset = Storage.objects.prefetch_related("storageposition_set").with_position_counts().order_by("order", "pk")
    permission_required = ["collect.view_storage"]


class StorageDetailView(PermissionRequiredMixin, DetailBreadcrumbsMixin, DetailView):
    model = Storage
    permission_required = ["collect.delete_storage"]

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
        RequestConfig(self.request).configure(table)
        context["table"] = table
        return context


class StorageSortView(PermissionRequiredMixin, SortableView):
    model = Storage
    permission_required = ["collect.change_storage"]


@permission_required("collect.add_storage", raise_exception=True)
def storage_create(request):
    form = StorageCreateForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        with transaction.atomic():
            storage = form.save()
            positions_count = form.cleaned_data["positions"]
            for i in range(positions_count):
                StoragePosition.objects.create(name=f"{i + 1}", storage=storage)
        if "btn-another" in request.POST:
            return redirect(reverse("collect:storage_create"))
        return redirect(reverse("collect:storage_detail", args=[storage.pk]))
    return TemplateResponse(request, "collect/storage_form.html", {"form": form})


@permission_required("collect.change_storage", raise_exception=True)
def storage_update(request, pk):
    instance = get_object_or_404(Storage, pk=pk)
    if request.method == "POST":
        form = StorageUpdateForm(request.POST, instance=instance)
        if form.is_valid():
            form.save()
            return redirect(reverse("collect:storage_detail", args=(instance.pk,)))
    form = StorageUpdateForm(instance=instance)
    return TemplateResponse(request, "frontpage/_update_form.html", {"form": form})


@permission_required("collect.delete_storage", raise_exception=True)
def storage_delete(request, pk):
    storage = get_object_or_404(Storage, pk=pk)

    if not storage.is_deletable():
        return redirect(reverse_lazy("collect:storage_list"))

    if request.POST:
        storage.delete()
        return redirect(reverse_lazy("collect:storage_list"))

    context = {"storage": storage, **generate_breadcrumbs(request, Storage, storage)}
    return TemplateResponse(request, "collect/storage_confirm_delete.html", context)


@permission_required("collect.add_sampleweight", raise_exception=True)
def sampleweight_create(request, sample_id):
    if request.method == "POST":
        form = SampleWeightForm(request.POST)
        if form.is_valid():
            sampleweight = form.save(commit=False)
            sampleweight.sample_id = sample_id
            sampleweight.save()
            return htmx_response_trigger_close_modal(["logItemUpdated"])
    else:
        form = SampleWeightForm()
    return TemplateResponse(
        request,
        "collect/partials/sampleweight_create.html",
        {"form": form},
    )


@permission_required("collect.change_sampleweight", raise_exception=True)
def sampleweight_update(request, pk):
    sampleweight = get_object_or_404(SampleWeight, pk=pk)
    if request.method == "POST":
        form = SampleWeightForm(request.POST, instance=sampleweight)
        if form.is_valid():
            form.save()
            return htmx_response_trigger_close_modal(["logItemUpdated"])

    else:
        form = SampleWeightForm(instance=sampleweight)
    return render(
        request,
        "collect/partials/sampleweight_update.html",
        {"sampleweight": sampleweight, "form": form},
    )


@permission_required("collect.delete_sampleweight", raise_exception=True)
def sampleweight_delete(request, pk):
    sampleweight = get_object_or_404(SampleWeight, pk=pk)
    if request.method == "POST":
        sampleweight.delete()
        return htmx_response_trigger_close_modal(["logItemUpdated"])
    return render(
        request,
        "collect/partials/sampleweight_confirm_delete.html",
        {},
    )


@permission_required("collect.add_germinability", raise_exception=True)
def germinability_create(request, sample_id):
    if request.method == "POST":
        form = GerminabilityForm(request.POST)
        if form.is_valid():
            germinability = form.save(commit=False)
            germinability.sample_id = sample_id
            germinability.save()
            return htmx_response_trigger_close_modal(["logItemUpdated"])
    else:
        form = GerminabilityForm()
    return TemplateResponse(
        request,
        "collect/partials/germinability_create.html",
        {"form": form},
    )


@permission_required("collect.change_germinability", raise_exception=True)
def germinability_update(request, pk):
    germinability = get_object_or_404(Germinability, pk=pk)
    if request.method == "POST":
        form = GerminabilityForm(request.POST, instance=germinability)
        if form.is_valid():
            form.save()
            return htmx_response_trigger_close_modal(["logItemUpdated"])
    else:
        form = GerminabilityForm(instance=germinability)
    return TemplateResponse(
        request,
        "collect/partials/germinability_update.html",
        {"germinability": germinability, "form": form},
    )


@permission_required("collect.delete_germinability", raise_exception=True)
def germinability_delete(request, pk):
    germinability = get_object_or_404(Germinability, pk=pk)
    if request.method == "POST":
        germinability.delete()
        return htmx_response_trigger_close_modal(["logItemUpdated"])
    return render(
        request,
        "collect/partials/germinability_confirm_delete.html",
        {},
    )
