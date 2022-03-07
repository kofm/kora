from django.shortcuts import render
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from collect.forms import SeedSampleForm

from collect.models import SeedSample, Storage
from register.models import PlantSpecies


class SeedSampleListView(ListView):
    model = SeedSample
    paginate_by = 10


class SeedSampleDetailView(DetailView):
    model = SeedSample
    context_object_name = 'sample'

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        # Add in a QuerySet of all the books
        context['storage_list'] = Storage.objects.all()
        return context

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
