from django.contrib.auth.decorators import permission_required, user_passes_test
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.db.models import Q
from django.http import HttpRequest
from django.shortcuts import get_object_or_404, redirect
from django.template.response import TemplateResponse
from django.urls.base import reverse_lazy
from django.views.decorators.http import require_http_methods
from django.views.generic import CreateView
from django.views.generic.edit import DeleteView, UpdateView
from django_tables2.config import RequestConfig

from breadcrumbs.generic import (
    DeleteBreadcrumbsMixin,
    UpdateBreadcrumbsMixin,
)
from breadcrumbs.utils import (
    add_plantvariety_breadcrumbs,
    generate_breadcrumbs,
)
from frontpage.views_decorators import (
    NavDescribeActiveContext,
    NavPlantActiveContext,
    htmx_render_blocks,
    nav_describe_active_context,
    nav_plant_active_context,
    public_catalog_view,
)
from register.filters import EntityFilter, ProtectionOmniFilter
from register.forms import EntityForm, ProtectionForm, ProtectionTypeForm
from register.models import Entity, PlantVariety, Protection, ProtectionType
from register.tables import EntityTable, PlantVarietyEntityTable, ProtectionListTable


@nav_plant_active_context
@public_catalog_view("register.view_protection")
@htmx_render_blocks(["main"])
def protection_list(request):
    queryset = Protection.objects.select_related("variety", "variety__species").all()
    flt = ProtectionOmniFilter(request.GET, queryset=queryset)
    table = ProtectionListTable(flt.qs)
    RequestConfig(request).configure(table)
    context = {"table": table, "filter": flt, **generate_breadcrumbs(request, Protection)}
    return TemplateResponse(request, "register/protection_list.html", context)


@nav_plant_active_context
@permission_required("register.add_protection", raise_exception=True)
def protection_create(request: HttpRequest, variety_id: int):
    variety = get_object_or_404(PlantVariety, pk=variety_id)
    if request.method == "POST":
        form = ProtectionForm(request.POST)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.variety = variety
            instance.save()
            form.save_m2m()
            return redirect(instance.get_absolute_url())
    to_dupe_pk = request.GET.get("duplicate")
    form = ProtectionForm()
    if to_dupe_pk:
        try:
            dupe = Protection.objects.get(pk=to_dupe_pk)
            initial = {
                "status": dupe.status,
                "country": dupe.country,
                "applicants": dupe.applicants.all(),
                "maintainers": dupe.maintainers.all(),
                "date_start": dupe.date_start,
                "date_end": dupe.date_end,
            }
            form = ProtectionForm(initial=initial)
        except Protection.DoesNotExist:
            pass
    context = {"form": form, "variety": variety, "model_name": "Protection"}
    breadcrumbs = generate_breadcrumbs(request, Protection)
    breadcrumbs = add_plantvariety_breadcrumbs(breadcrumbs, variety)
    context.update(breadcrumbs)
    return TemplateResponse(request, "frontpage/_create_form.html", context)


@nav_plant_active_context
@permission_required("register.change_protection", raise_exception=True)
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
    context = {"form": form, "object": protection, "variety": protection.variety}
    breadcrumbs = generate_breadcrumbs(request, Protection, protection)
    breadcrumbs = add_plantvariety_breadcrumbs(breadcrumbs, protection.variety)
    context.update(breadcrumbs)
    return TemplateResponse(request, "frontpage/_update_form.html", context)


class ProtectionDeleteView(PermissionRequiredMixin, DeleteBreadcrumbsMixin, NavPlantActiveContext, DeleteView):
    object: Protection
    model = Protection
    permission_required = ["register.delete_protection"]
    success_url = reverse_lazy("register:protection_list")


@nav_plant_active_context
@public_catalog_view("register.view_protection")
def protection_detail(request, pk):
    instance = get_object_or_404(Protection, pk=pk)
    breadcrumbs = generate_breadcrumbs(request, Protection, instance)
    breadcrumbs = add_plantvariety_breadcrumbs(breadcrumbs, instance.variety)
    return TemplateResponse(
        request,
        "register/protection_detail.html",
        {"protection": instance, **breadcrumbs},
    )


@user_passes_test(lambda user: user.is_staff)
def protection_configure(request):
    form = ProtectionTypeForm(request.POST or None)
    if form.is_valid():
        form.save()
    protection_types = ProtectionType.objects.order_by("pk")
    context = {"form": form, "protection_types": protection_types}
    return TemplateResponse(request, "register/protection_configure.html", context)


@user_passes_test(lambda user: user.is_staff)
def protection_type_update(request, pk):
    instance = get_object_or_404(ProtectionType, pk=pk)
    form = ProtectionTypeForm(request.POST or None, instance=instance)
    if form.is_valid():
        form.save()
        return redirect("register:protection_configure")
    context = {"instance": instance, "form": form}
    return TemplateResponse(request, "register/partials/protection_type_update.html", context)


@user_passes_test(lambda user: user.is_staff)
@require_http_methods(["POST"])
def protection_type_delete(request, pk):
    instance = get_object_or_404(ProtectionType, pk=pk)
    instance.delete()
    return redirect("register:protection_configure")


class EntityCreateView(PermissionRequiredMixin, CreateView):
    model = Entity
    form_class = EntityForm
    template_name = "frontpage/modal_form.html"
    permission_required = ["register.add_entity"]

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context["object_to_create"] = "Entity"
        return context


@nav_describe_active_context
@public_catalog_view("register.view_entity")
def entity_detail(request, pk):
    entity = get_object_or_404(Entity, pk=pk)
    query = Q()
    query |= Q(protection__applicants=pk)
    query |= Q(protection__maintainers=pk)
    qs = PlantVariety.objects.select_related("species").prefetch_related("protection_set").filter(query).distinct()
    table = PlantVarietyEntityTable(qs)
    RequestConfig(request).configure(table)
    context = {"entity": entity, "table": table, **generate_breadcrumbs(request, Entity, entity)}
    return TemplateResponse(request, "register/entity_detail.html", context)


class EntityUpdateView(PermissionRequiredMixin, UpdateBreadcrumbsMixin, NavDescribeActiveContext, UpdateView):
    model = Entity
    form_class = EntityForm
    template_name = "frontpage/_update_form.html"
    permission_required = ["register.change_entity"]


class EntityDeleteView(PermissionRequiredMixin, NavDescribeActiveContext, DeleteView):
    object: Entity
    model = Entity
    template_name = "frontpage/confirm_delete.html"
    permission_required = ["register.delete_entity"]
    success_url = reverse_lazy("register:entity_list")


@nav_describe_active_context
@public_catalog_view("register.view_entity")
@htmx_render_blocks(["main"])
def entity_list(request):
    flt = EntityFilter(request.GET, queryset=Entity.objects.all())
    table = EntityTable(flt.qs)
    RequestConfig(request).configure(table)
    context = {"table": table, "filter": flt}
    context.update(generate_breadcrumbs(request, Entity))
    return TemplateResponse(request, "register/entity_list.html", context)
