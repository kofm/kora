"""Protocol views."""

from django.contrib.auth.decorators import permission_required
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render
from django.template.response import TemplateResponse
from django.urls import reverse
from django.urls.base import reverse_lazy
from django.views.generic.edit import CreateView, DeleteView

from breadcrumbs.generic import (
    CreateBreadcrumbsMixin,
    DeleteBreadcrumbsMixin,
)
from breadcrumbs.utils import generate_breadcrumbs
from describe.forms import ProtocolMetadataForm, StateFormSet, TraitForm
from describe.models import Protocol
from django_sortable_htmx.views import SortableView
from frontpage.views_decorators import (
    NavDescribeActiveContext,
    nav_describe_active_context,
)


def protocol_list(request):
    context = {}
    context["object_list"] = Protocol.objects.select_related("plantspecies").all()
    context.update(generate_breadcrumbs(request, Protocol))
    return TemplateResponse(request, "describe/protocol_list.html", context)


class ProtocolSortView(PermissionRequiredMixin, SortableView):
    model = Protocol
    permission_required = ["describe.change_protocol"]


def protocol_detail(request, pk):
    instance = Protocol.objects.select_related("plantspecies").prefetch_related("traits__states").get(pk=pk)
    context = {"protocol": instance}
    context.update(generate_breadcrumbs(request, Protocol, instance))
    return TemplateResponse(request, "describe/protocol_detail.html", context)


@nav_describe_active_context
@permission_required("describe.change_protocol", raise_exception=True)
def protocol_update(request, pk):
    context = {}
    protocol = get_object_or_404(Protocol.objects.prefetch_related("traits"), pk=pk)
    trait = protocol.traits.first()
    if trait:
        context["trait_next"] = trait.get_next_in_protocol()
        context["trait_prev"] = trait.get_previous_in_protocol()
        form = TraitForm(instance=trait)
        context["formset"] = StateFormSet(instance=trait)
    else:
        form = TraitForm(initial={"protocol": protocol})
    context.update(
        {
            "protocol": protocol,
            "object": protocol,
            "title": protocol.name,
            "subtitle": protocol.plantspecies,
            "current_trait": trait,
            "form": form,
        }
    )
    context.update(generate_breadcrumbs(request, Protocol, protocol))
    return render(request, "describe/protocol_update.html", context)


class ProtocolCreate(CreateBreadcrumbsMixin, NavDescribeActiveContext, CreateView):
    model = Protocol
    fields = ["name", "plantspecies", "url_ref"]
    template_name = "frontpage/_create_form.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["model_name"] = "Protocol"
        return context

    def get_success_url(self):
        return reverse("describe:protocol_update", args=(self.object.id,))


def protocol_update_meta(request, pk):
    instance = get_object_or_404(Protocol, pk=pk)
    if request.method == "POST":
        form = ProtocolMetadataForm(request.POST, instance=instance)
        if form.is_valid():
            form.save()
            return HttpResponse(headers={"HX-Redirect": reverse("describe:protocol_update", args=(instance.pk,))})
    else:
        form = ProtocolMetadataForm(instance=instance)
    context = {"protocol": instance, "form": form}
    return TemplateResponse(request, "describe/partials/protocol_update_metadata.html", context)


class ProtocolDelete(PermissionRequiredMixin, DeleteBreadcrumbsMixin, NavDescribeActiveContext, DeleteView):
    model = Protocol
    success_url = reverse_lazy("describe:protocol_list")
    permission_required = ["describe.delete_protocol"]
