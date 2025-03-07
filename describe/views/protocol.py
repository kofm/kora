"""Protocol views."""

from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render
from django.template.response import TemplateResponse
from django.urls import reverse
from django.urls.base import reverse_lazy
from django.views.generic import DetailView, ListView
from django.views.generic.edit import CreateView, DeleteView
from django_tables2 import RequestConfig

from breadcrumbs.generic import (
    CreateBreadcrumbsMixin,
    DeleteBreadcrumbsMixin,
    DetailBreadcrumbsMixin,
    ListBreadcrumbsMixin,
)
from breadcrumbs.utils import generate_breadcrumbs
from describe.forms import ProtocolMetadataForm, StateFormSet, TraitForm
from describe.models import Protocol, Trait
from describe.tables import ProtocolTable
from frontpage.views_decorators import (
    NavDescribeActiveContext,
    nav_describe_active_context,
)


class ProtocolList(ListBreadcrumbsMixin, NavDescribeActiveContext, ListView):
    model = Protocol
    context_object_name = "protocols"

    def get_queryset(self):
        return Protocol.objects.select_related("plantspecies").all()

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        table = ProtocolTable(self.get_queryset())
        RequestConfig(self.request, paginate={"per_page": 15}).configure(table)
        context["table"] = table
        return context


class ProtocolDetail(DetailBreadcrumbsMixin, NavDescribeActiveContext, DetailView):
    model = Protocol


@nav_describe_active_context
def protocol_update(request, pk):
    context = {}
    protocol = get_object_or_404(Protocol, pk=pk)
    trait: Trait = protocol.traits.first()
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
            "subtitle": protocol.plantspecies.latin_name,
            "current_trait": trait,
            "form": form,
        }
    )
    context.update(generate_breadcrumbs(request, Protocol, protocol))
    return render(request, "describe/protocol_update.html", context)


class ProtocolCreate(CreateBreadcrumbsMixin, NavDescribeActiveContext, CreateView):
    """View to create a new Protocol."""

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


class ProtocolDelete(DeleteBreadcrumbsMixin, NavDescribeActiveContext, DeleteView):
    model = Protocol
    success_url = reverse_lazy("describe:protocol_list")
