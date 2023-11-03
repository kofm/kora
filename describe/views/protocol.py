"""
Protocol views
"""

from describe.forms import ProtocolNameForm, TraitFormSet
from describe.models import Protocol
from django.http.response import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import get_object_or_404, render
from django.template.response import TemplateResponse
from django.urls import reverse
from django.urls.base import reverse_lazy
from django.utils.html import format_html
from django.views.generic import DetailView, ListView
from django.views.generic.edit import CreateView, DeleteView

from frontpage.decorators import NavActive, nav_active


class NavActiveDescribe(NavActive):
    def __init__(self) -> None:
        super().__init__("nav_describe")


def protocol_list(request, species_id):
    """Endpoint for the list of protocols by species.
    This is the endpoint used to fetch the protocols list for the
    tom-select input in protocol_form.html
    """
    queryset = list(
        Protocol.objects.filter(plantspecies__variety=species_id).values("pk", "name")
    )
    return JsonResponse(queryset, safe=False)


class ProtocolList(NavActiveDescribe, ListView):
    model = Protocol
    template_name = "describe/protocols_list.html"
    context_object_name = "protocols"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["nav_protocols"] = "active"
        return context


class ProtocolDetail(NavActiveDescribe, DetailView):
    model = Protocol
    context_object_name = "protocol"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["nav_protocols"] = "active"
        return context


@nav_active("nav_describe")
def protocol_detail(request, pk):
    context = {}
    protocol = get_object_or_404(Protocol, pk=pk)
    context["protocol"] = protocol
    return TemplateResponse(request, "describe/protocol_detail.html", context)


def protocol_update(request, pk):
    protocol = get_object_or_404(Protocol, pk=pk)
    if request.method == "POST":
        form = TraitFormSet(request.POST, instance=protocol)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(
                reverse("describe:protocol_detail", kwargs={"pk": protocol.pk})
            )
    else:
        form = TraitFormSet(instance=protocol)
    return render(
        request,
        "describe/protocol_manage.html",
        {"fs": form, "protocol": protocol, "nav_protocols": "active"},
    )


def protocol_update_name_htmx(request, pk):
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


class ProtocolCreate(NavActiveDescribe, CreateView):
    model = Protocol
    fields = [
        "name",
        "plantspecies",
        "url_ref",
    ]
    template_name = "describe/protocol_form.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["nav_protocols"] = "active"
        return context

    def get_success_url(self):
        return reverse("describe:protocol-update", args=(self.object.id,))


class ProtocolDelete(DeleteView):
    model = Protocol
    success_url = reverse_lazy("describe:protocols_list")
