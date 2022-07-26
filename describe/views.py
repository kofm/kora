from django.db.models.expressions import F
from django.forms.models import model_to_dict
from django.http.response import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.template.response import TemplateResponse
from django.urls import reverse
from django.urls.base import reverse_lazy
from django.views.generic import DetailView, ListView
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django_tables2 import RequestConfig
from describe.forms import (
    DescriptionFilterFormSet,
    ExpressionForm,
    ProtocolForm,
    TraitFormSet,
)
from describe.tables import DescriptionTable
from register.utils import paged_object_list_context

from .models import Description, Expression, Protocol, State, Trait


def get_first_item_by_key(list, value, key):
    return next(filter(lambda x: x[key] == value, list))


def merge_unique(base, addition, key):
    addition_keys = [x[key] for x in addition]
    return [
        get_first_item_by_key(addition, list_item[key], key)
        if list_item[key] in addition_keys
        else list_item
        for list_item in base
    ]


def description_list(request):
    """
    Renders a list of variety descriptions. It also handles filtering by traits
    within a specific protocol.
    Tasks:
    1. Get the protocol and display the filter
    2. Process the filter and store into session
    """
    context = dict()

    if "protocol" in request.session:
        protocol = request.session.get("protocol")
    else:
        protocol = Protocol.objects.most_used()

    traits = Trait.objects.filter(protocol=protocol).values(trait=F("pk"))
    formset = DescriptionFilterFormSet(initial=traits)

    queryset = Description.objects.all().prefetch_related("expressions")

    if request.POST:
        formset = DescriptionFilterFormSet(request.POST, initial=traits)
        request.session["description_filter"] = list()
        if formset.is_valid():
            for form in formset:
                if states := form.cleaned_data["state"]:
                    queryset = queryset.filter(expressions__state__in=states)
                    request.session["description_filter"].append(
                        {
                            "trait": form.cleaned_data["trait"],
                            "state": [state.pk for state in states],
                        }
                    )
    elif "description_filter" in request.session:
        for expression in request.session["description_filter"]:
            queryset = queryset.filter(expressions__state__in=expression["state"])

        formset = DescriptionFilterFormSet(
            initial=merge_unique(
                traits, request.session.get("description_filter"), "trait"
            )
        )

    protocol_form = ProtocolForm(initial={"protocol": protocol})
    # context.update(paged_object_list_context(request, queryset, paginate_by=10))
    description_table = DescriptionTable(queryset)
    RequestConfig(request).configure(description_table)
    context.update(
        {
            "formset": formset,
            "protocol_form": protocol_form,
            "page_obj": description_table,
        }
    )

    return TemplateResponse(request, "describe/description_list.html", context)


class DescriptionDetail(DetailView):
    model = Description
    context_object_name = "description"


class DescriptionDeleteView(DeleteView):
    model = Description
    success_url = reverse_lazy("describe:description-list")


class ProtocolsList(ListView):
    model = Protocol
    template_name = "describe/protocols_list.html"
    context_object_name = "protocols"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["nav_protocols"] = "active"
        return context


class ProtocolCreate(CreateView):
    model = Protocol
    fields = [
        "name",
        "specie",
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


class ProtocolDetail(DetailView):
    model = Protocol
    context_object_name = "protocol"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["nav_protocols"] = "active"
        return context


def protocol_update(request, pk):
    protocol = get_object_or_404(Protocol, pk=pk)
    if request.method == "POST":
        form = TraitFormSet(request.POST, instance=protocol)
        # form = TraitForm(request.POST)
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


def description_update(request, pk):
    # Get the description object
    description = get_object_or_404(Description, pk=pk)
    # Collect all the existing expressions
    exist_expr = description.expressions.all()
    # This is the forms list
    forms = []
    if request.method == "POST":
        form_has_errors = False
        for expr_id, state_id in zip(
            request.POST.getlist("id"), request.POST.getlist("state")
        ):
            if state_id:
                form = ExpressionForm({"id": expr_id, "state": state_id})
                if form.is_valid():
                    # __import__('pdb').set_trace()
                    # expression, create = Expression.objects.get_or_create(**form.cleaned_data, description = description)
                    if exist_expr.filter(
                        pk=form.cleaned_data["id"]
                    ).exists() and not exist_expr.filter(
                        state=form.cleaned_data["state"]
                    ):
                        exist_expr.filter(pk=form.cleaned_data["id"]).update(
                            state=form.cleaned_data["state"]
                        )
                        print("Updated existing")
                    else:
                        if not exist_expr.filter(state=form.cleaned_data["state"]):
                            new_expression = Expression()
                            new_expression.state = form.cleaned_data["state"]
                            new_expression.description = description
                            new_expression.save()
                            print("Created new")
                else:
                    form_has_errors = True
            else:
                if expr_id:
                    exist_expr.filter(pk=expr_id).delete()
                    print("Deleted")
        if not form_has_errors:
            return HttpResponseRedirect(
                reverse("describe:description_detail", args=(description.id,))
            )

    for trait in description.available_traits:
        if exist_expr.filter(state__trait=trait).exists():
            e = exist_expr.get(state__trait=trait)
            form = ExpressionForm(model_to_dict(e))
        else:
            form = ExpressionForm()
        form.fields["state"].queryset = State.objects.filter(trait=trait)
        forms.append(form)
    formset = zip(forms, description.available_traits)
    return render(
        request, "describe/description_manage.html", context={"formset": formset}
    )


class ExpressionUpdate(UpdateView):
    model = Expression
    fields = "__all__"
    template_name = "describe/expression_update.html"


class DescriptionCreate(CreateView):
    model = Description
    fields = [
        "name",
        "protocol",
        "variety",
    ]
    template_name = "describe/description_form.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["nav_descriptions"] = "active"
        return context

    def get_success_url(self):
        return reverse("describe:description-update", args=(self.object.id,))
