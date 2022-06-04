# pyright: reportGexeralTypeIssues=false
from django.http.response import HttpResponse
from django.shortcuts import get_object_or_404
from django.template.response import TemplateResponse
from django.urls.base import reverse_lazy
from django.views.decorators.http import require_http_methods
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, DeleteView
from calculator.forms import CropModelForm, CropParameterForm, ManagementForm
from calculator.models import Crop, Management
from calculator.utils import get_crop_params_list, get_cropmodels
from register.models import PlantSpecies

"""Register CropModels here"""
CROP_MODELS = [
    "PhenologyCropModel",
    "CropModelExpectedYield",
    "CropModelTotalPlants",
]


class CropDetailView(DetailView):
    model = Crop


class CropDeleteView(DeleteView):
    model = Crop

    def get_success_url(self):
        return reverse_lazy("spaces:area-detail", kwargs={"pk": self.object.area.pk})


def crop_update_view(request, pk):
    # Get the crop
    crop = get_object_or_404(Crop, pk=pk)

    if request.POST:
        form = CropModelForm(request.POST, instance=crop)
        if form.is_valid():
            form.save()
            if any(x in form.changed_data for x in ["species", "variety"]):
                crop.parameters.all().delete()

    # Instantiate the form
    form = CropModelForm(
        instance=crop,
        initial={
            "area": crop.area,
            "sowing": crop.sowing,
            "harvest": crop.harvest,
            "notes": crop.notes,
        },
    )

    # Set initial value depending on the set crop
    # import pdb; pdb.set_trace()
    if crop.has_variety():
        form.initial["species"] = crop.variety.species.pk
        form.initial["variety"] = crop.variety.pk
    elif crop.has_species():
        form.initial["species"] = crop.species.pk

    cropparameter_form = CropParameterForm(initial={"crop": crop})

    # JSON data to populate the species tom-select
    plantspecies = list(PlantSpecies.objects.all().values("pk", "common_name"))
    cropparameter_table = get_crop_params_list(crop)
    context = {
        "crop": crop,
        "form": form,
        "plantspecies": plantspecies,
        "cropparameter_table": cropparameter_table,
        "cropparameter_form": cropparameter_form,
    }
    context.update(get_cropmodels(crop, CROP_MODELS))
    return TemplateResponse(request, "calculator/crop_update.html", context)


@require_http_methods(
    [
        "POST",
    ]
)
def cropparam_update_hx(request, pk):
    context = {}
    form = CropParameterForm(request.POST)
    crop = get_object_or_404(Crop, pk=pk)
    if form.is_valid():
        form.save()
    # context["cropparameter_table"] = CropParameterTable(get_crop_params_list(crop))
    context["cropparameter_table"] = get_crop_params_list(crop)
    context["cropparameter_form"] = form
    context["crop"] = crop
    context.update(get_cropmodels(crop, CROP_MODELS))
    return TemplateResponse(
        request, "calculator/partials/cropparams_collapse.html", context
    )


def cropparam_value(request):
    form = CropParameterForm(initial=request.GET)
    print(form)
    return HttpResponse(form["value"])

class CropCreateView(CreateView):
    form_class = CropModelForm
    model = Crop
    template_name = "calculator/crop_update.html"

    def get_success_url(self):
        return reverse_lazy("calculator:crop-update", kwargs={"pk": self.object.pk})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["plantspecies"] = list(
            PlantSpecies.objects.all().values("pk", "common_name")
        )
        return context

    def get_initial(self):
        initial = super().get_initial()
        initial = initial.copy()
        area = self.kwargs["area_id"]
        if area:
            initial["area"] = area
        return initial


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
