from django.shortcuts import render
from django.urls.base import reverse
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.views.generic.list import ListView
from rest_framework.decorators import api_view
from rest_framework import status
from rest_framework.response import Response
from collect.forms import SeedSampleForm

from collect.models import Germinability, SampleWeight, SeedSample, Storage, StoragePosition
from collect.serializers import GerminabilitySerializer, SampleWeightSerializer, SeedSampleSerializer, StoragePositionSerializer
from register.models import PlantSpecies, PlantVariety

class StorageCreateView(CreateView):
    model = Storage
    fields = ['name', ]

class SeedSampleListView(ListView):
    model = SeedSample
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["storage_list"] = Storage.objects.all()
        return context


class SeedSampleDetailView(DetailView):
    model = SeedSample
    context_object_name = "sample"

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        context["storage_list"] = Storage.objects.filter(storageposition__seedsample__isnull=True)
        context["variety_list"] = PlantVariety.objects.all()
        context["sample_form"] = SeedSampleForm(instance=self.object)
        return context

class SeedSampleDeleteView(DeleteView):
    model = SeedSample

class SeedSampleUpdateView(UpdateView):
    form_class = SeedSampleForm
    model = SeedSample

class SeedSampleCreateView(CreateView):
    form_class = SeedSampleForm
    model = SeedSample

    def get_success_url(self):
        if "btn-another" in self.request.POST:
            return reverse('collect:seedsample-create')
        return super().get_success_url()

@api_view(['PUT'])
def seedsample_update(request, pk):
    try:
        seedsample = SeedSample.objects.get(pk=pk)
    except SeedSample.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    if request.method == 'PUT':
        serializer = SeedSampleSerializer(seedsample, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def fetch_storagepositions(request, pk):
    if request.method == 'GET':
        storagepositions = StoragePosition.objects.filter(storage_id=pk, seedsample__isnull=True)
        serializer = StoragePositionSerializer(storagepositions, many=True)
        return Response(serializer.data)

def seedsample_create(request):
    plantspecies = PlantSpecies.objects.values("pk", "common_name")
    form = SeedSampleForm()
    return render(
        request,
        "collect/seedsample_create.html",
        {
            "plantspecies": plantspecies,
            "form": form,
        },
    )

@api_view(['GET', 'POST'])
def germinability(request):
    if request.method == 'GET':
        snippets = Germinability.objects.all()
        serializer = GerminabilitySerializer(snippets, many=True)
        return Response(serializer.data)
    if request.method == 'POST':
        serializer = GerminabilitySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'POST'])
def sample_weight(request):
    if request.method == 'GET':
        snippets = SampleWeight.objects.all()
        serializer = SampleWeightSerializer(snippets, many=True)
        return Response(serializer.data)
    if request.method == 'POST':
        serializer = SampleWeightSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
