from django.db.models.expressions import F
from django.forms.models import model_to_dict
from django.http.response import HttpResponse, HttpResponseRedirect
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
    RelatedStateForm,
    TraitFormSet,
)
from describe.tables import DescriptionTable, RelatedStatesTable
from describe.utils import _filter_descriptions, merge_unique

from .models import Description, Expression, Protocol, State, Trait

"""
Descriptions
List, Detail, Update, Create, Delete
"""

def reset_description_filter(request):
    try:
        del request.session["description_filter"]
    except KeyError:
        pass

def description_list(request):
    """List of Descriptions
    Filter descriptions by state of expression(s) according to the selected reference protocol
    """
    context = dict()

    if request.GET and "reset" in request.GET:
        reset_description_filter(request)

    if protocol_set:= request.GET.get("protocol", None):
        request.session["protocol"] = protocol_set
        reset_description_filter(request)

    # TODO: this will break if there are no Protocol in the database
    protocol_id = request.session.get("protocol", Protocol.objects.most_used().pk)

    protocol = Protocol.objects.get(pk=protocol_id)
    traits = Trait.objects.filter(protocol=protocol).values(trait=F("pk"))
    formset = DescriptionFilterFormSet(initial=traits)

    queryset = Description.objects.filter().prefetch_related("expressions")

    if request.POST:
        formset = DescriptionFilterFormSet(request.POST, initial=traits)
        request.session["description_filter"] = list()
        if formset.is_valid():
            for form in formset:
                if states := form.cleaned_data["state"]:
                    queryset = _filter_descriptions(queryset, states)
                    request.session["description_filter"].append(
                        {
                            "trait": form.cleaned_data["trait"],
                            "state": [state.pk for state in states],
                        }
                    )
    elif "description_filter" in request.session:
        for expression in request.session["description_filter"]:
            queryset = _filter_descriptions(queryset, expression["state"])

        formset = DescriptionFilterFormSet(
            initial=merge_unique(
                traits, request.session.get("description_filter"), "trait"
            )
        )

    protocol_form = ProtocolForm(initial={"protocol": protocol})
    description_table = DescriptionTable(queryset)
    RequestConfig(request, paginate={"per_page": 15}).configure(description_table)

    if request.htmx:
        base_template = "describe/description_list_partial.html"
    else:
        base_template = "describe/description_list_base.html"

    context.update(
        {
            "formset": formset,
            "protocol_form": protocol_form,
            "page_obj": description_table,
            "page_template": base_template,
        }
    )

    return TemplateResponse(request, "describe/description_list.html", context)


class DescriptionDetail(DetailView):
    model = Description
    context_object_name = "description"


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


class DescriptionDeleteView(DeleteView):
    model = Description
    success_url = reverse_lazy("describe:description-list")


def description_filter_export(request):
    """
    Endpoint to export the current filter and the matching
    descriptions as text.
    """
    from datetime import datetime

    filter = request.session.get("description_filter", None)
    protocol = request.session.get("protocol", None)
    filename = f"description_filter_{datetime.today().strftime('%Y%m%d%H%M%S')}.txt"
    text = [
        "There is no filter set, yet.",
    ]

    if filter and protocol:
        queryset = Description.objects.all().prefetch_related("expressions")
        text = list()
        text.append("# Current search:")
        text.append("")
        text.append(f"Protocol: {Protocol.objects.get(pk=protocol)}")
        text.append("")
        for f in filter:
            text.append(Trait.objects.get(pk=f["trait"]).__str__())
            text.extend([f"\t { State.objects.get(pk=s) }" for s in f["state"]])
            queryset = _filter_descriptions(queryset, f["state"])
        text.append("")
        text.append("---")
        text.append("")
        text.append(f"# Found descriptions ({ queryset.count() }):")
        text.append("")
        text.extend([f"- {description}" for description in queryset])

    response = HttpResponse("\n".join(text), content_type="text/plain; charset=utf-8")
    response["Content-Disposition"] = "attachment; filename={0}".format(filename)
    return response


"""
Protocol
"""


class ProtocolsList(ListView):
    model = Protocol
    template_name = "describe/protocols_list.html"
    context_object_name = "protocols"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["nav_protocols"] = "active"
        return context


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


class ProtocolCreate(CreateView):
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


"""
Trait
"""


def trait_list_htmx(request):
    """
    This is accessed by HTMX requests made by RelatedStateForm to populate the
    Trait/State select input, depending on the selected Protocol/Trait
    """
    if request.htmx:
        form = RelatedStateForm(request.GET)
        if "protocol" in request.GET:
            return HttpResponse(form["trait"])
        else:
            return HttpResponse(form["related_state"])


"""
State
"""


def state_update(request, pk):
    context = {}
    state = get_object_or_404(State, pk=pk)
    context["state"] = state

    if request.method == "POST":
        relatedstate_form = RelatedStateForm(request.POST)
        if relatedstate_form.is_valid():
            related_state = State.objects.get(
                pk=relatedstate_form["related_state"].value()
            )
            state.related_states.add(related_state)
            relatedstate_form = RelatedStateForm(initial={"state": state.pk})
    else:
        relatedstate_form = RelatedStateForm(initial={"state": state.pk})
    context["relatedstate_form"] = relatedstate_form
    context["relatedstates_table"] = RelatedStatesTable(state.related_states.all())
    return TemplateResponse(request, "describe/state_form.html", context)


def relatedstate_delete(request, pk):
    state = get_object_or_404(State, pk=pk)
    related_state = request.GET.get("related_state", None)
    if related_state:
        state.related_states.remove(State.objects.get(pk=related_state))
    return HttpResponse()


"""
Expression
"""


class ExpressionUpdate(UpdateView):
    model = Expression
    fields = "__all__"
    template_name = "describe/expression_update.html"
