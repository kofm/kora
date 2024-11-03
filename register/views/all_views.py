from django_tables2.config import RequestConfig

from breadcrumbs.generic import (
    CreateBreadcrumbsMixin,
    CrumbsCreateView,
    UpdateBreadcrumbsMixin,
)
from breadcrumbs.utils import detail_crumb, generate_breadcrumbs, list_crumb
from django.shortcuts import get_object_or_404, redirect
from django.template.response import TemplateResponse
from django.urls import reverse
from django.urls.base import reverse_lazy
from django.views.generic import CreateView, DetailView
from django.views.generic.edit import DeleteView, UpdateView
from parameters.forms import VarietalParameterForm
from parameters.models import VarietalParameter
from register.filters import EntityFilter
from register.forms import ProtectionForm
from register.models import Entity, PlantVariety, Protection
from register.tables import EntityTable, PlantVarietyEntityTable
from register.views.base_views import NavPlantActiveContext, nav_active_plants


class PlantVarietyParametersList(NavPlantActiveContext, DetailView):
    model = PlantVariety
    context_object_name = "variety"
    template_name = "register/plantvarietyparameters_list.html"


class VarietalParameterCreate(NavPlantActiveContext, CrumbsCreateView):
    model = VarietalParameter
    form_class = VarietalParameterForm
    template_name_suffix = "_create_form"

    @property
    def crumbs(self):
        return [list_crumb(self.variety._meta.model), detail_crumb(self.variety), ("Create Parameter", None)]

    @property
    def variety(self):
        return PlantVariety.objects.get(pk=self.kwargs.get("pk"))

    def get_initial(self, *args, **kwargs):
        initial_data = super().get_initial(*args, **kwargs)
        initial_data.update({"variety": self.variety})
        return initial_data

    def get_success_url(self, *args, **kwargs):
        return reverse("register:plantvarietyparameters_list", kwargs={"pk": self.variety.pk})


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


class EntityCreateView(CreateBreadcrumbsMixin, CreateView):
    model = Entity
    fields = "__all__"
    template_name = "frontpage/_create_form.html"

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context["model_name"] = "Entity"
        return context


@nav_active_plants
def entity_detail(request, pk):
    entity = get_object_or_404(Entity, pk=pk)
    table = PlantVarietyEntityTable(entity.plantvariety_set.all())
    RequestConfig(request, paginate={"per_page": 10}).configure(table)
    context = {"entity": entity, "table": table}
    context.update(generate_breadcrumbs(Entity, entity))
    return TemplateResponse(request, "register/entity_detail.html", context)


class EntityUpdateView(UpdateBreadcrumbsMixin, NavPlantActiveContext, UpdateView):
    model = Entity
    fields = "__all__"
    template_name = "frontpage/_update_form.html"


@nav_active_plants
def entity_list(request):
    context = {}
    filter = EntityFilter(request.GET, queryset=Entity.objects.all())
    table = EntityTable(filter.qs)
    RequestConfig(request, paginate={"per_page": 25}).configure(table)
    context["table"] = table
    context["filter"] = filter
    context.update(generate_breadcrumbs(Entity))
    return TemplateResponse(request, "register/entity_list.html", context)
