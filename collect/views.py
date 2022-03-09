from django.shortcuts import render
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from rest_framework.decorators import api_view
from rest_framework.response import Response
from collect.forms import SeedSampleForm

from collect.models import SeedSample, Storage, StoragePosition
from collect.serializers import StoragePositionSerializer
from register.models import PlantSpecies, PlantVariety


class SeedSampleListView(ListView):
    model = SeedSample
    paginate_by = 10


class SeedSampleDetailView(DetailView):
    model = SeedSample
    context_object_name = "sample"

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        # Add in a QuerySet of all the books
        context["storage_list"] = Storage.objects.filter(storageposition__seedsample__isnull=True)
        context["variety_list"] = PlantVariety.objects.all()
        return context


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
