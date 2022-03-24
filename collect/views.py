from django.urls.base import reverse
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.views.generic.list import ListView
from rest_framework.decorators import api_view
from rest_framework import status, viewsets
from rest_framework.response import Response
from collect.forms import SeedSampleForm

from collect.models import (
    Germinability,
    SampleWeight,
    SeedSample,
    Storage,
)
from collect.serializers import (
    GerminabilitySerializer,
    SampleWeightSerializer,
    SeedSampleSerializer,
)
from register.models import PlantVariety


class StorageCreateView(CreateView):
    model = Storage
    fields = [
        "name",
    ]


class SeedSampleListView(ListView):
    model = SeedSample
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

    def get_queryset(self):
        search = self.request.GET.get("search")
        if search and search != '':
            if len(search) < 2:
                queryset = SeedSample.objects.filter(variety__names__name__istartswith=search)
            else:
                queryset = SeedSample.objects.filter(variety__names__name__unaccent__lower__trigram_similar=search)
        else:
            queryset = SeedSample.objects.all()
        return queryset

    def get_storages(self):
        queryset = Storage.objects.all()
        paginator = Paginator(queryset, 5)
        page = self.request.GET.get("storage_page")
        storages = paginator.get_page(page)
        return storages


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

    def get_success_url(self):
        if "btn-another" in self.request.POST:
            return reverse("collect:seedsample-create")
        return super().get_success_url()


class SeedSampleUpdateView(UpdateView):
    form_class = SeedSampleForm
    model = SeedSample


class SeedSampleDeleteView(DeleteView):
    model = SeedSample

class StorageListView(ListView):
    model = Storage
    paginate_by = 10


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
