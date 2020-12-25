from django.shortcuts import get_object_or_404, reverse
from django.http import HttpResponse
from django.views.generic import ListView,DetailView,CreateView,View,FormView
from django.views.generic.edit import FormMixin
from django.views.generic.detail import SingleObjectMixin
from .models import PlantSpecies,PlantVariety
from .forms import PlantSpeciesForm, PlantVarietyForm

class PlantSpeciesList(ListView):
    model = PlantSpecies

class PlantSpeciesCreate(CreateView):
    model = PlantSpecies
    form_class = PlantSpeciesForm
    context_object_name = 'species'
    success_url = "/register/species/"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["plantspecies_list"] = PlantSpecies.objects.all()
        return context

class PlantSpeciesDetail(DetailView):
    model = PlantSpecies
    context_object_name = 'species'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = PlantVarietyForm()
        return context

    def post(self, request, *args, **kwargs):
        new_variety = PlantVariety(name = request.POST.get('name'),
                species=self.get_object())
        new_variety.save()
        return self.get(self, request, *args, **kwargs)

class PSDetail(FormMixin, DetailView):
    model = PlantSpecies
    form_class = PlantVarietyForm
    template_name = "register/plantspecies_detail.html"
    context_object_name = 'species'

    def get_initial(self):
        return {"species": self.get_object()}

    def get_success_url(self):
        return reverse("register:plantspecie_detail", kwargs={"pk": self.object.pk})

    def get_context_data(self, **kwargs):
        context = super(PSDetail, self).get_context_data(**kwargs)
        context["form"] = self.get_form()
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_valid(self, form):
        plant_variety = PlantVariety(**form.cleaned_data)
        plant_variety.save()
        return super().form_valid(form)

class PlantVarietyDetail(DetailView):
    model = PlantVariety
    context_object_name = 'variety'




def debug_request(request):
    return HttpResponse(request)
