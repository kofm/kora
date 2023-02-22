from django.views.decorators.http import require_http_methods
from django_filters.views import FilterView
import csv
from typing import Any, Dict
from django.core.paginator import Paginator
from django.db.models.aggregates import Max, Sum
from django.db.models.expressions import Value
from django.db.models.functions import Cast
from django.db.models.functions.text import Concat
from django.db.models import IntegerField, Count
from django.db.models.query import QuerySet
from django.db.models.query_utils import Q
from django.http.response import HttpResponse
from django.shortcuts import get_object_or_404, render
from django.utils.timezone import now
from django.urls.base import reverse, reverse_lazy
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.views.generic.list import ListView
from django_tables2.views import SingleTableMixin, SingleTableView
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from collect.filters import SeedSampleFilter
from collect.forms import (
    GerminabilityForm,
    SampleWeightForm,
    SeedSampleForm,
)

from collect.models import (
    Cart,
    Germinability,
    SampleWeight,
    SeedSample,
    Storage,
    StoragePosition,
)
from collect.serializers import (
    GerminabilitySerializer,
    SampleWeightSerializer,
)
from collect.tables import SeedSampleTable
from register.models import PlantVarietyName


class StorageCreateView(CreateView):
    model = Storage
    fields = [
        "name",
    ]


class SeedSampleListView(SingleTableMixin, FilterView):
    queryset = SeedSample.objects.all()
    filterset_class = SeedSampleFilter
    table_class = SeedSampleTable
    template_name = ''
    paginate_by = 15

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.user.is_authenticated:
            cart = get_object_or_404(Cart, user=self.request.user, active=True)
            context["cart"] = cart
        return context

    def get_template_names(self):
        if self.request.htmx:
            template_name = "collect/partials/seedsample_table.html"
        else:
            template_name = "collect/seedsample_list.html"

        return template_name


    

class SeedSampleDetailView(DetailView):
    model = SeedSample
    context_object_name = "sample"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        duplicate_samples = self.object.duplicate_samples
        context["duplicate_samples_table"] = SeedSampleTable(duplicate_samples)
        context["seedsample_weight_form"] = SampleWeightForm()
        return context

@require_http_methods(['POST',])
def sampleweight_create_hx(request, pk):
    seedsample = get_object_or_404(SeedSample, pk=pk)
    form=SampleWeightForm(request.POST)
    if form.is_valid():
        seedsample_weight = form.save(commit=False)
        seedsample_weight.seedsample = seedsample
        seedsample_weight.save()
        form=SampleWeightForm()
    return render(
        request,
        "collect/partials/seedsample_weight_form.html",
        {
            'seedsample_weight_form': form,
            'seedsample': seedsample
        }
    )


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
