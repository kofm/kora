from django_tables2.config import RequestConfig

from django.core.paginator import Paginator
from django.http.response import HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect
from django.template.response import TemplateResponse
from django.urls.base import reverse, reverse_lazy
from django.views.generic import CreateView, DetailView
from django.views.generic.edit import DeleteView, UpdateView
from parameters.forms import SpeciesParameterForm, VarietalParameterForm
from register.filters import EntityFilter
from register.forms import ProtectionForm
from register.models import Entity, PlantSpecies, PlantVariety, Protection
from register.tables import EntityTable, PlantVarietyEntityTable
from register.views.base_views import NavPlantActiveContext, nav_active_plants


class PlantSpeciesParametersList(NavPlantActiveContext, DetailView):
    model = PlantSpecies
    context_object_name = "species"
    template_name = "register/plantspeciesparameters_list.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        parameters = self.get_related_parameters()
        context["nav_species"] = "active"
        context["parameters"] = parameters
        return context

    def get_related_parameters(self):
        queryset = self.object.parameters.all()
        paginator = Paginator(queryset, 5)
        page = self.request.GET.get("page")
        parameters = paginator.get_page(page)
        return parameters


class PlantVarietyParametersList(NavPlantActiveContext, DetailView):
    model = PlantVariety
    context_object_name = "variety"
    template_name = "register/plantvarietyparameters_list.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["nav_species"] = "active"
        return context


@nav_active_plants
def add_speciesparametervervalue(request, pk):
    """
    https://stackoverflow.com/questions/37303171/django-create-new-object-in-form-update-select-box-and-save-it
    https://stackoverflow.com/questions/7782479/django-reverse-engineering-the-admin-sites-add-foreign-key-button
    Check this to add new parameter without leaving this view
    """
    species = PlantSpecies.objects.get(pk=pk)
    form = SpeciesParameterForm(initial={"specie": species})
    if request.method == "POST":
        form = SpeciesParameterForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse("register:plantspeciesparameters_list", kwargs={"pk": species.id}))

    context = {"form": form}
    return TemplateResponse(request, "register/plantspeciesparameters_create.html", context)


@nav_active_plants
def add_varietalparamevterervalue(request, pk):
    variety = PlantVariety.objects.get(pk=pk)
    form = VarietalParameterForm(initial={"variety": variety})
    if request.method == "POST":
        form = VarietalParameterForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect(reverse("register:plantvarietyparameters_list", kwargs={"pk": variety.id}))

    context = {"form": form}
    return TemplateResponse(request, "register/plantspeciesparameters_create.html", context)


@nav_active_plants
def protection_create(request, variety_id):
    variety = get_object_or_404(PlantVariety, pk=variety_id)
    if request.POST:
        form = ProtectionForm(request.POST)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.variety = variety
            instance.save()
            form.save_m2m()
            return redirect(instance.get_absolute_url())
    duplicate_id = request.GET.get("duplicate")
    form = ProtectionForm()
    if duplicate_id:
        try:
            protection_to_duplicate = Protection.objects.get(pk=duplicate_id)
            initial = {}
            initial["status"] = protection_to_duplicate.status
            initial["country"] = protection_to_duplicate.country
            initial["applicants"] = protection_to_duplicate.applicants.all()
            initial["maintainers"] = protection_to_duplicate.maintainers.all()
            initial["date_start"] = protection_to_duplicate.date_start
            initial["date_end"] = protection_to_duplicate.date_end
            form = ProtectionForm(initial=initial)
        except Protection.DoesNotExist:
            pass
    return TemplateResponse(
        request,
        "register/protection_form.html",
        {
            "form": form,
            "variety": variety,
        },
    )


@nav_active_plants
def protection_update(request, pk):
    context = {}
    protection = get_object_or_404(Protection, pk=pk)
    if request.method == "POST":
        form = ProtectionForm(request.POST, instance=protection)
        if form.is_valid():
            instance = form.save()
            return redirect(instance.get_absolute_url())
    else:
        form = ProtectionForm(instance=protection)
        context["form"] = form
        context["protection"] = protection
        context["variety"] = protection.variety
    return TemplateResponse(request, "register/protection_form.html", context)


class ProtectionDeleteView(DeleteView):
    model = Protection

    def get_success_url(self):
        return reverse_lazy("register:plantvariety_detail", args=[self.object.variety.pk])


class ProtectionDetailView(NavPlantActiveContext, DetailView):
    model = Protection


class EntityCreateView(CreateView):
    model = Entity
    fields = "__all__"


@nav_active_plants
def entity_detail(request, pk):
    context = {}
    entity = get_object_or_404(Entity, pk=pk)
    context["entity"] = entity
    context["varieties_table"] = PlantVarietyEntityTable(entity.plantvariety_set.all())
    return TemplateResponse(request, "register/entity_detail.html", context)


class EntityUpdateView(NavPlantActiveContext, UpdateView):
    model = Entity
    fields = "__all__"


@nav_active_plants
def entity_list(request):
    context = {}
    filter = EntityFilter(request.GET, queryset=Entity.objects.all())
    table = EntityTable(filter.qs)
    RequestConfig(request, paginate={"per_page": 25}).configure(table)
    context["table"] = table
    context["filter"] = filter
    return TemplateResponse(request, "register/entity_list.html", context)
