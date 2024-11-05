"""Protocol views."""

from breadcrumbs.generic import (
    CreateBreadcrumbsMixin,
    DeleteBreadcrumbsMixin,
    DetailBreadcrumbsMixin,
    ListBreadcrumbsMixin,
)
from breadcrumbs.utils import generate_breadcrumbs
from describe.forms import ProtocolNameForm, TraitFormSet
from describe.models import Protocol
from django.http.response import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.template.response import TemplateResponse
from django.urls import reverse
from django.urls.base import reverse_lazy
from django.utils.html import format_html
from django.views.generic import DetailView, ListView
from django.views.generic.edit import CreateView, DeleteView
from frontpage.views_decorators import NavDescribeActiveContext


class ProtocolList(ListBreadcrumbsMixin, NavDescribeActiveContext, ListView):
    model = Protocol
    context_object_name = "protocols"


class ProtocolDetail(DetailBreadcrumbsMixin, NavDescribeActiveContext, DetailView):
    model = Protocol


def protocol_update(request, pk):
    protocol = get_object_or_404(Protocol, pk=pk)
    if request.method == "POST":
        form = TraitFormSet(request.POST, instance=protocol)
        if form.is_valid():
            form.save()
            return redirect(reverse("describe:protocol_detail", kwargs={"pk": protocol.pk}))
    else:
        form = TraitFormSet(instance=protocol)
    context = {"fs": form, "protocol": protocol, "nav_protocols": "active"}
    context.update(generate_breadcrumbs(request, Protocol, protocol))
    return render(request, "describe/protocol_manage.html", context)


def protocol_update_name_htmx(request, pk):
    """HTMX view to update the name of a Protocol."""
    protocol = get_object_or_404(Protocol, pk=pk)
    template = "describe/partials/protocol_name_form.html"
    form = ProtocolNameForm(instance=protocol)
    if request.POST:
        form = ProtocolNameForm(request.POST, instance=protocol)
        if form.is_valid():
            protocol = form.save()
            return HttpResponse(
                format_html(
                    '<h1 class="display-1" hx-get="{}" hx-trigger="click" \
                    hx-swap="outerHTML">{}</h1>',
                    reverse("describe:protocol-updatename", kwargs={"pk": protocol.pk}),
                    protocol.name,
                )
            )
    return TemplateResponse(request, template, {"form": form, "protocol": protocol})


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


class ProtocolDelete(DeleteBreadcrumbsMixin, NavDescribeActiveContext, DeleteView):
    model = Protocol
    success_url = reverse_lazy("describe:protocol_list")
