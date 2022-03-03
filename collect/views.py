from django.shortcuts import render
from django.views.generic.list import ListView
from collect.forms import SeedSampleForm

from collect.models import SeedSample
from register.models import PlantSpecies

class SeedSamplesList(ListView):
    model=SeedSample
    paginate_by=10

def seedsample_create(request):
    plantspecies=PlantSpecies.objects.values('pk', 'common_name')
    form=SeedSampleForm()
    return render(
        request,
        'collect/seedsample_create.html',
        {
            'plantspecies': plantspecies,
            'form': form,
        }
    )
