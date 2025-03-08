"""Description Views.

List, Detail, Update, Create, Delete
"""

import contextlib

from django.db.models import CharField, Q
from django.db.models.expressions import F
from django.db.models.functions import Lower
from django.http import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404, redirect
from django.template.response import TemplateResponse
from django.urls import reverse_lazy
from django.views.decorators.http import require_GET
from django.views.generic import DeleteView, DetailView
from django_tables2 import RequestConfig

from breadcrumbs.generic import DeleteBreadcrumbsMixin
from breadcrumbs.utils import generate_breadcrumbs
from describe.filters import DescriptionFilterByName
from describe.forms import (
    DescriptionFilterFormSet,
    DescriptionForm,
    DescriptionUpdateForm,
    ExpressionForm,
    ProtocolForm,
    TraitStatesFormSet,
)
from describe.models import (
    Description,
    Expression,
    Protocol,
    State,
    Trait,
)
from describe.tables import DescriptionTable
from describe.utils import (
    _filter_descriptions,
    delete_get_param,
    merge_unique,
)
from describe.views.protocol import NavDescribeActiveContext
from frontpage.views_decorators import nav_active
from register.models import PlantVariety

CharField.register_lookup(Lower)

nav_describe = nav_active("nav_describe")


def process_formset(formset):
    expressions_filter = []

    for form in formset:
        if form.is_valid() and form.cleaned_data.get("selected_states"):
            expressions_filter.append({"state": form.cleaned_data["selected_states"]})
    return expressions_filter


@nav_describe
def description_list(request):
    context = {}

    descriptions = Description.objects.with_expressions().all()
    expressions_filter = None
    base_template = "describe/description_list_partial.html" if request.htmx else "describe/description_list_base.html"

    context.update(generate_breadcrumbs(request, Description))

    traits = Trait.objects.filter(protocol=7).prefetch_related("states").order_by("pk")[:2]

    if request.method == "POST":
        formset = TraitStatesFormSet(request.POST, traits=traits)
        if formset.is_valid():
            expressions_filter = process_formset(formset)

    if expressions_filter:
        descriptions = descriptions.filter_by_expressions(expressions_filter)

    table = DescriptionTable(descriptions)
    RequestConfig(request, paginate={"per_page": 10}).configure(table)

    context.update({"page_obj": table, "page_template": base_template})

    return TemplateResponse(request, "describe/description_list.html", context)


def description_filter(request):
    traits = Trait.objects.filter(protocol=7).prefetch_related("states").order_by("pk")[:2]
    if request.method == "POST":
        formset = TraitStatesFormSet(request.POST, traits=traits)
    else:
        formset = TraitStatesFormSet(traits=traits)  # type: ignore[call-arg]
    return TemplateResponse(request, "describe/partials/description_filter.html", {"formset": formset})


@nav_describe
def description_list_old(request):
    """List Descriptions.

    Filter descriptions by state of expression(s) according to the
    selected reference protocol."""
    context = {}

    # Check if the protocol has changed; if yes, set the session variable and
    # reset the filter to operate with the newly selected protocol.
    protocol_set = request.GET.get("protocol", None)
    if protocol_set:
        request.session["protocol"] = protocol_set
        reset_description_filter(request)
        request.GET = delete_get_param(request, "protocol")

    # Check if the protocol session variable is set, otherwise set it to the
    # most used Protocol
    protocol_id = request.session.get("protocol", None)
    if not protocol_id:
        most_used_protocol = Protocol.objects.most_used()
        if most_used_protocol:
            protocol_id = most_used_protocol.pk
            request.session["protocol"] = protocol_id

    protocol_select_form = ProtocolForm()
    traits = Trait.objects.all()

    if request.session and "protocol" in request.session:
        # Get the selected/default Protocol
        protocol = get_object_or_404(Protocol, pk=protocol_id)
        # Instantiate the Protocol selection form
        protocol_select_form = ProtocolForm(initial={"protocol": protocol})

        # Get all the Traits associated with that Protocol
        traits = Trait.objects.filter(protocol=protocol).values(trait=F("pk"))

        # If the Description filter has been submitted via post, validate the
        # formset and assign the returned filter to the appropriate session
        # variable
    if request.POST:
        formset = DescriptionFilterFormSet(request.POST, initial=traits)
        if formset.is_valid():
            request.session["description_filter"] = formset.save()

    if request.session.get("description_filter", None):
        # If a Description filter session variable exists, get the matching
        # Descriptions and instantiate the formset with the corresponding data
        queryset = Description.objects.filter_by_expressions(request.session.get("description_filter"))
        # Merge unique is needed here because we need all the available traits
        # merged with the actual filter. If we pass description_filter alone
        # the formset will be instantiated with only the filtered traits
        formset = DescriptionFilterFormSet(
            initial=merge_unique(traits, request.session.get("description_filter"), "trait")
        )
    else:
        # Otherwise return all the available descriptions and instantiate an empty
        # Description filter formset
        queryset = Description.objects.filter().prefetch_related("expressions")
        formset = DescriptionFilterFormSet(initial=traits)

    description_filter_by_name = DescriptionFilterByName(request.GET, queryset=queryset)
    # Instantiate the Descriptions table and corresponding pagination
    description_table = DescriptionTable(
        description_filter_by_name.qs.select_related("variety", "protocol", "variety__species")
    )
    RequestConfig(request, paginate={"per_page": 10}).configure(description_table)

    # Check if the current request is an htmx request, then render only the
    # relevant part of the page; otherwise return the full page

    base_template = "describe/description_list_partial.html" if request.htmx else "describe/description_list_base.html"

    context.update(generate_breadcrumbs(request, Description))

    context.update(
        {
            "description_filter_by_name": description_filter_by_name,
            "formset": formset,
            "protocol_form": protocol_select_form,
            "page_obj": description_table,
            "page_template": base_template,
        }
    )

    return TemplateResponse(request, "describe/description_list.html", context)


def reset_description_filter(request):
    with contextlib.suppress(KeyError):
        del request.session["description_filter"]


def description_filter_export(request):
    """Export current filter and the matching descriptions as plain text."""
    from datetime import datetime

    description_filter = request.session.get("description_filter", None)
    protocol = request.session.get("protocol", None)
    curtime = datetime.today().strftime("%Y%m%d%H%M%S")
    filename = f"description_filter_{curtime}.txt"
    text = [
        "There is no filter set, yet.",
    ]

    if description_filter and protocol:
        queryset = Description.objects.all().prefetch_related("expressions")
        text = list()
        text.append("==========================")
        text.append("Description Search")
        text.append("==========================")
        text.append("")
        text.append(f"Protocol: {Protocol.objects.get(pk=protocol)}")
        text.append("")
        for f in description_filter:
            text.append(Trait.objects.get(pk=f["trait"]).__str__())
            text.extend([f"\t {State.objects.get(pk=s)}" for s in f["state"]])
            queryset = _filter_descriptions(queryset, f["state"])
        text.append("")
        text.append("=========================")
        text.append(f"Results ({queryset.count()}):")
        text.append("=========================")
        text.append("")
        text.extend([f"- {description}" for description in queryset])

    response = HttpResponse("\n".join(text), content_type="text/plain; charset=utf-8")
    response["Content-Disposition"] = f"attachment; filename={filename}"
    return response


@require_GET
def description_list_reset(request):
    reset_description_filter(request)
    return redirect(reverse_lazy("describe:description_list"))


def description_find_similar(request):
    """Find similar Descriptions according to the 'grouping' criteria.

    Get a description_id as input and set the description filter with
    the grouping characteristics of the description."""
    description_id = request.GET.get("description_id", None)

    if description_id:
        description_filter = Expression.objects.filter(
            description__pk=description_id, state__trait__grouping=True
        ).values(trait=F("state__trait"), states=F("state"))
        # Transform the filter to ease querying with __in
        request.session["description_filter"] = [
            {
                "trait": filt["trait"],
                "state": [
                    filt["states"],
                ],
            }
            for filt in list(description_filter)
        ]
    return redirect(reverse_lazy("describe:description_list"))


@nav_describe
def description_compare(request):
    context = {}
    active_list = request.user.workspace_set.filter(is_active=True).first()

    if not active_list:
        return JsonResponse({"error": "No active description list found."}, status=400)

    elements = active_list.descriptions.select_related("description").all()
    descriptions = [element.description for element in elements]

    if not descriptions:
        context.update({"comparison_table_header": [], "comparison_table": []})
        return TemplateResponse(request, "describe/description_compare.html", context)

    protocols = Protocol.objects.filter(descriptions__in=descriptions).distinct()

    comparison_table = [{"protocol": protocol.name, "rows": []} for protocol in protocols]
    comparison_table_header = [f"{description.variety.name} - {description.name}" for description in descriptions]

    for protocol_index, protocol in enumerate(protocols):
        for trait in protocol.traits.all():
            row = [f"{trait.numeric_id}. {trait.description}"]
            expression_ids = []

            for description in descriptions:
                expressions = description.expressions.filter(
                    Q(state__trait=trait) | Q(state__related_states__trait=trait)
                )

                if expressions.exists():
                    expression = expressions.last()
                    expression_id = expression.state.numeric_id
                    row.append(f"{expression_id}. {expression.state.description}")
                    expression_ids.append(expression_id)
                else:
                    row.append("")

            rows_equal = all([id == expression_ids[0] for id in expression_ids]) if expression_ids else False
            comparison_table[protocol_index]["rows"].append({"values": row, "equal": rows_equal})

    context.update({"comparison_table_header": comparison_table_header, "comparison_table": comparison_table})

    return TemplateResponse(request, "describe/description_compare.html", context)


class DescriptionDetail(NavDescribeActiveContext, DetailView):
    model = Description
    context_object_name = "description"


@nav_describe
def description_update(request, pk):
    description = get_object_or_404(Description, pk=pk)
    form = DescriptionUpdateForm(request.POST or None, instance=description)

    if form.is_valid():
        description = form.save()
        return redirect(description.get_absolute_url())
    context = {"form": form, "object": description, "description": description}
    context.update(generate_breadcrumbs(request, Description, description))
    return TemplateResponse(
        request,
        "describe/description_update.html",
        context,
    )


@nav_describe
def description_create(request):
    context = {}

    form = DescriptionForm(request.POST or None)
    if form.is_valid():
        description = form.save()
        return redirect(description.get_absolute_url())

    variety_id = request.GET.get("variety_id", None)
    if variety_id:
        variety = get_object_or_404(PlantVariety, pk=variety_id)
        form.initial["variety"] = variety
        context["variety"] = variety
    context["form"] = form
    context["model_name"] = "Description"
    context.update(generate_breadcrumbs(request, Description))

    return TemplateResponse(request, "describe/description_create.html", context)


class DescriptionDeleteView(DeleteBreadcrumbsMixin, NavDescribeActiveContext, DeleteView):
    model = Description
    success_url = reverse_lazy("describe:description_list")


def description_expression_update(request, pk):
    description = get_object_or_404(Description, pk=pk)
    traits = description.available_traits
    formset = []

    for trait in traits:
        expressions = description.expressions.filter(state__trait=trait)
        forms = []
        if expressions.exists():
            for expression in expressions:
                form = ExpressionForm(instance=expression, trait=trait)
                forms.append(form)
        formset.append({"trait": trait, "forms": forms})
    context = {"description": description, "formset": formset}
    context.update(generate_breadcrumbs(request, Description, description))
    return TemplateResponse(
        request,
        "describe/description_expression_update.html",
        context,
    )
