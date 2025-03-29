"""Description Views.

List, Detail, Update, Create, Delete
"""

from collections import defaultdict
from datetime import datetime

from django.contrib.auth.decorators import login_required
from django.db.models import CharField
from django.db.models.functions import Lower
from django.forms import BaseFormSet
from django.http import HttpRequest, HttpResponse
from django.shortcuts import get_object_or_404, redirect
from django.template.response import TemplateResponse
from django.urls import reverse, reverse_lazy
from django.views.generic import DeleteView
from django_tables2 import RequestConfig
from render_block import render_block_to_string

from breadcrumbs.generic import DeleteBreadcrumbsMixin
from breadcrumbs.utils import add_plantvariety_breadcrumbs, generate_breadcrumbs
from describe.forms import (
    DescriptionFilterForm,
    DescriptionForm,
    DescriptionUpdateForm,
    ExpressionFilterFormSet,
    ExpressionForm,
    ProtocolForm,
    ProtocolStrictSearchForm,
)
from describe.models import (
    Description,
    Expression,
    Protocol,
    State,
    Workspace,
    WorkspaceElement,
)
from describe.tables import DescriptionTable
from describe.views.protocol import NavDescribeActiveContext
from describe.views.utils import (
    make_descriptions_dict,
    make_species_descriptions_dict,
    make_species_protocols_dict,
    make_traits_expressions_dict,
)
from frontpage.views_decorators import nav_active
from register.filters import filter_name_generic
from register.models import PlantVariety

CharField.register_lookup(Lower)

nav_describe = nav_active("nav_describe")


def _get_description_form(request: HttpRequest):
    """Create (and eventually process) `DescriptionFilterForm`.

    Return the form instance
    """
    if request.method == "POST":
        form = DescriptionFilterForm(request.POST)
    else:
        form = DescriptionFilterForm()

    form.fields["variety"].widget.attrs["hx-trigger"] = "keyup changed delay:500ms"
    form.fields["variety"].widget.attrs["hx-post"] = reverse("describe:description_list")
    return form


def _get_protocol_form(request: HttpRequest, protocol=None) -> tuple[ProtocolForm, Protocol]:
    """Create and process `ProtocolForm`.

    Returns the form instance and a `Protocol` instance. If the form
    wasn't submitted, return the most used protocol as default.
    """
    protocol = protocol or Protocol.objects.most_used()

    if request.method == "POST":
        form = ProtocolForm(request.POST)
        if form.is_valid():
            protocol = form.cleaned_data.get("protocol")
    else:
        form = ProtocolForm(initial={"protocol": protocol})
    return (form, protocol)


def description_filter_name_variety(descriptions, form_description):
    """Applies filter according to `DescriptionFilterForm` to the
    input Description QuerySet.

    Returns the (eventually) filtered QuerySet.
    """

    if not form_description.is_valid():
        return descriptions

    description_variety_name = form_description.cleaned_data["variety"]
    description_name = form_description.cleaned_data["name"]

    if description_variety_name:
        descriptions = filter_name_generic(
            descriptions.select_related("variety"), "variety__name", description_variety_name
        )
    if description_name:
        descriptions = descriptions.filter(name__in=description_name)

    return descriptions


def _get_strict_search_form(request: HttpRequest) -> tuple[ProtocolStrictSearchForm, bool]:
    result = False
    form = ProtocolStrictSearchForm()
    if request.method == "POST":
        form = ProtocolStrictSearchForm(request.POST)
        if form.is_valid():
            result = form.cleaned_data.get("strict")  # type: ignore
    return (form, result)


def _get_expression_filter(request: HttpRequest, protocol: Protocol) -> tuple[BaseFormSet, list]:
    """Process `ExpressionFilterFormSet` and return a list of
    expressions to filter by.

    The returned list is intended to be used with
    `Description.objects.filter_by_expressions()`.
    """
    traits = protocol.with_traits_and_states()
    formset = ExpressionFilterFormSet(traits=traits)  # type: ignore[call-arg]
    result: list = []
    if request.method != "POST":
        return (formset, result)

    formset = ExpressionFilterFormSet(request.POST, traits=traits)  # type: ignore[call-arg]
    if formset.is_valid():
        result = formset.get_expression_ids()  # type: ignore[attr-defined]
    return (formset, result)


def _get_description_asterisked_expression(description_id):
    return Expression.objects.prefetch_related("state__trait").filter(
        description=description_id, state__trait__grouping=True
    )


def _render_header(string):
    return [
        "",
        "==========================",
        string,
        "==========================",
        "",
    ]


def _render_filter_expression_to_text(filter_expression):
    states = [state for states in filter_expression for state in states]
    states = (
        State.objects.filter(pk__in=states)
        .select_related("trait")
        .values("trait__numeric_id", "trait__description", "numeric_id", "description")
    )

    output = defaultdict(list)
    for state in states:
        trait_id = state["trait__numeric_id"]
        trait = state["trait__description"]
        state_id = state["numeric_id"]
        state = state["description"]

        output[f"{trait_id}. {trait}"].append(f"{state_id}. {state}")

    text = _render_header(f"Expression Filters ({len(filter_expression)})")
    for trait, states in output.items():
        text.append(trait)

        for state in states:
            text.append(f"    {state}")
    return text


def _render_search_info(protocol):
    return _render_header("Description Search") + [
        f"Protocol: {protocol.name}",
    ]


def _render_description_list(descriptions):
    header = _render_header(f"Results ({descriptions.count()}):")
    body = [f"- {description}" for description in descriptions]
    return header + body


def _render_export_file_to_response(protocol, filter_expression, descriptions):
    text = (
        _render_search_info(protocol)
        + _render_filter_expression_to_text(filter_expression)
        + _render_description_list(descriptions)
    )
    curtime = datetime.today().strftime("%Y%m%d%H%M%S")
    filename = f"description_filter_{curtime}.txt"
    response = HttpResponse("\n".join(text), content_type="text/plain")
    response["Content-Disposition"] = f"attachment; filename={filename}"
    return response


@nav_describe
def description_list(request):
    context = {}
    template_name = "describe/description_list.html"

    descriptions = Description.objects.with_expressions()
    form_protocol_filter, protocol = _get_protocol_form(request)
    form_description = _get_description_form(request)
    form_strict_search, filter_strict = _get_strict_search_form(request)
    formset_expression, filter_expression = _get_expression_filter(request, protocol)

    descriptions = description_filter_name_variety(descriptions, form_description)

    if filter_strict:
        descriptions = descriptions.filter(protocol=protocol)

    if filter_expression:
        descriptions = descriptions.filter_by_expressions(filter_expression)

    if request.method == "POST" and "export" in request.POST:
        return _render_export_file_to_response(protocol, filter_expression, descriptions)

    table = DescriptionTable(descriptions)
    RequestConfig(request, paginate={"per_page": 10}).configure(table)
    context.update({"table": table})

    if request.headers.get("HX-Request") == "true":
        rendered_block = render_block_to_string(
            template_name,
            "description_table",
            context,
            request,
        )
        return HttpResponse(rendered_block)

    context.update(generate_breadcrumbs(request, Description))
    context.update(
        {
            "form": form_protocol_filter,
            "form_description": form_description,
            "formset": formset_expression,
            "form_strict_search": form_strict_search,
        }
    )

    return TemplateResponse(request, template_name, context)


def description_filter(request):
    template_name = ("describe/description_list.html",)
    form, protocol = _get_protocol_form(request)
    form_strict_search, _ = _get_strict_search_form(request)
    traits = protocol.with_traits_and_states()
    formset = ExpressionFilterFormSet(traits=traits)
    context = {"form_strict_search": form_strict_search, "formset": formset}
    rendered_block = render_block_to_string(
        template_name,
        block_name="expression_filter",
        context=context,
        request=request,
    )
    return HttpResponse(content=rendered_block)


def _make_filter_from_expressions(expressions):
    filter_expression = defaultdict(list)
    for e in expressions:
        filter_expression[e.state.trait.pk].append(e.state.pk)
    return list(filter_expression.values())


def description_find_similar(request):
    """Populate filter form with similar traits based on a reference description."""

    template_name = "describe/description_list.html"

    description_id = request.GET.get("description_id")
    description = get_object_or_404(Description, pk=description_id)

    form_protocol_filter, protocol = _get_protocol_form(request, description.protocol)
    form_strict_search, filter_strict = _get_strict_search_form(request)

    traits = protocol.with_traits_and_states()
    expressions = _get_description_asterisked_expression(description_id)

    filter_expression = _make_filter_from_expressions(expressions)

    formset_expression = ExpressionFilterFormSet(expressions=expressions, traits=traits)

    form_description_filter = _get_description_form(request)

    descriptions = Description.objects.with_expressions().filter_by_expressions(filter_expression)
    table = DescriptionTable(descriptions)
    RequestConfig(request, paginate={"per_page": 10}).configure(table)

    if request.headers.get("HX-Request") == "true":
        protocol_response = render_block_to_string(
            template_name,
            "protocol_select",
            {"form": form_protocol_filter},
            request=request,
        )
        table_response = render_block_to_string(
            template_name,
            "description_table",
            {"table": table},
            request=request,
        )

        filter_response = render_block_to_string(
            template_name,
            "expression_filter",
            {"form_strict_search": form_strict_search, "formset": formset_expression},
            request=request,
        )
        return HttpResponse(filter_response + protocol_response + table_response)

    context = {
        "table": table,
        "form": form_protocol_filter,
        "form_description": form_description_filter,
        "formset": formset_expression,
        "form_strict_search": form_strict_search,
    }
    context.update(generate_breadcrumbs(request, Description))

    return TemplateResponse(request, "describe/description_list.html", context)


@nav_describe
@login_required
def description_compare(request):
    wsp = Workspace.objects.filter(user=request.user, is_active=True).first()
    elems = WorkspaceElement.objects.select_related("description__variety__species").filter(workspace=wsp)
    names = elems.order_by("description__name").values_list("description__name", flat=True).distinct()
    varieties = elems.order_by("description__variety__id").values_list("description__variety__id", flat=True).distinct()

    # Get all the available Descriptions for any of the Variety-Name
    # combinations present in the workspace.
    # This includes descriptions from other protocols, too.
    descriptions = Description.objects.filter(variety__in=varieties, name__in=names)

    protocols = (
        Protocol.objects.select_related("plantspecies")
        .prefetch_related("traits__states")
        .filter(descriptions__in=descriptions)
    )

    descriptions_dictionary = make_species_descriptions_dict(descriptions)
    compare_table = make_species_protocols_dict(protocols, descriptions_dictionary)

    context = {"compare_table": compare_table, "workspace": wsp}
    context.update(generate_breadcrumbs(request, Workspace, wsp))

    return TemplateResponse(
        request,
        "describe/description_compare.html",
        context,
    )


def description_detail(request, pk):
    description = Description.objects.select_related("variety", "protocol").get(pk=pk)

    description_annotated = Description.objects.annotated().filter(pk=pk)
    description_dict = make_descriptions_dict(description_annotated)
    protocol = Protocol.objects.get(descriptions=pk)
    traits = protocol.with_traits_and_states()
    table = make_traits_expressions_dict(traits, description_dict)

    context = {"description": description, "table": table}
    breadcrumbs = generate_breadcrumbs(request, Description, description)
    breadcrumbs = add_plantvariety_breadcrumbs(breadcrumbs, description.variety)

    context.update(breadcrumbs)

    return TemplateResponse(request, "describe/description_detail.html", context)


@nav_describe
def description_update(request, pk):
    description = get_object_or_404(Description, pk=pk)
    form = DescriptionUpdateForm(request.POST or None, instance=description)
    if form.is_valid():
        description = form.save()
        return redirect(description.get_absolute_url())

    context = {"form": form, "object": description, "description": description}
    context.update(generate_breadcrumbs(request, Description, description))
    return TemplateResponse(request, "describe/description_update.html", context)


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
    return TemplateResponse(request, "describe/description_expression_update.html", context)
