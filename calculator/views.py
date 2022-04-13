# pyright: reportGeneralTypeIssues=false
import importlib
from django.shortcuts import get_object_or_404, render
from django.urls.base import reverse_lazy
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, DeleteView
from calculator.forms import CropForm, ManagementForm
from calculator.models import Crop, Management
from register.models import PlantSpecies

"""Register CropModels here"""
CROP_MODELS = [
    # 'CropModelExpectedYield',
    # 'CropModelTotalPlants',
    "PhenologyCropModel"
]


class CropDetailView(DetailView):
    model = Crop


class CropDeleteView(DeleteView):
    model = Crop
    success_url = reverse_lazy("spaces:locations_list")

def crop_update_view(request, pk):
    # Get the crop
    crop = get_object_or_404(Crop, pk=pk)

    if request.POST:
        form = CropForm(request.POST)
        if form.is_valid():
            variety = form.cleaned_data["variety"]
            species = form.cleaned_data["species"]
            area = form.cleaned_data["area"]
            sowing = form.cleaned_data["sowing"]
            harvest = form.cleaned_data["harvest"]
            notes = form.cleaned_data["notes"]
            crop.area = area
            crop.notes = notes
            if variety:
                crop.set_crop(variety, "plantvariety")
            else:
                crop.set_crop(species, "plantspecies")

            if sowing:
                crop.sowing = sowing
            elif crop.sowing:
                del crop.sowing
            if harvest:
                crop.harvest = harvest
            elif crop.harvest:
                del crop.harvest

            crop.save()
            crop.parameters.all().delete()

    # Instantiate the form
    form = CropForm(
        initial={
            "area": crop.area,
            "sowing": crop.sowing,
            "harvest": crop.harvest,
            "notes": crop.notes,
        }
    )
    if crop.has_species():
        form.initial["species"] = crop.object_id
    elif crop.has_variety():
        form.initial["species"] = crop.content_object.species.id # type: ignore
        form.initial["variety"] = crop.object_id

    module = importlib.import_module("calculator.cropmodels")
    cropmodels = []
    for cm in CROP_MODELS:
        class_ = getattr(module, cm)
        m = class_(crop)  # type: ignore
        if m.can_run():
            cropmodels.append(m.output())
    # JSON data to populate the species tom-select
    plantspecies = list(PlantSpecies.objects.all().values("pk", "common_name"))
    return render(
        request,
        "calculator/crop_update.html",
        {"crop": crop, "form": form, "plantspecies": plantspecies, "cropmodels": cropmodels, },
    )


class ManagementCreateView(CreateView):
    model = Management
    form_class = ManagementForm

    def get_success_url(self):
        return reverse_lazy("calculator:crop-update", args=[self.kwargs["pk"]])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["crop"] = Crop.objects.get(pk=self.kwargs["pk"])
        return context

    def form_valid(self, form):
        crop = Crop.objects.get(pk=self.kwargs["pk"])
        self.object = form.save(commit=False)
        self.object.crop = crop
        self.object.save()
        return super().form_valid(form)
