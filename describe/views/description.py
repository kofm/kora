"""Description Views.

List, Detail, Update, Create, Delete
"""

from collections import defaultdict

from django.contrib.auth.decorators import login_required
from django.db.models import CharField
from django.db.models.functions import Lower
from django.http import HttpResponse, HttpResponseBadRequest
from django.shortcuts import get_object_or_404, redirect
from django.template.response import TemplateResponse
from django.urls import reverse, reverse_lazy
from django.views.decorators.http import require_POST
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
from describe.models import Description, Protocol, Trait, Workspace, WorkspaceElement
from describe.tables import DescriptionTable
from describe.views.protocol import NavDescribeActiveContext
from describe.views.utils import (
    get_description_asterisked_expression,
    get_protocol_form,
    get_strict_search_form,
    init_description_filter,
    make_descriptions_dict,
    make_species_descriptions_dict,
    make_species_protocols_dict,
    make_traits_expressions_dict,
)
from frontpage.views_decorators import nav_active
from register.models import PlantVariety

CharField.register_lookup(Lower)

nav_describe = nav_active("nav_describe")


def reset_filters(request):
    if "description_filter" in request.session:
        del request.session["description_filter"]


@nav_describe
def description_list(request):
    context = {}

    if not request.headers.get("HX-Request") == "true":
        reset_filters(request)

    template_name = "describe/description_list.html"

    descriptions = Description.objects.with_expressions()

    description_filter = init_description_filter(request)
    protocol_id = description_filter["protocol"]
    expression_filter = description_filter["expressions"]
    name_filter = description_filter["name"]
    strict_filter = description_filter["strict"]

    form_protocol = ProtocolForm(initial={"protocol": protocol_id})
    form_name = DescriptionFilterForm(initial={"name": name_filter})
    form_strict = ProtocolStrictSearchForm(initial={"strict": strict_filter})
    traits = Trait.objects.filter(protocol=protocol_id).with_states()
    formset = ExpressionFilterFormSet(traits=traits, expressions=expression_filter)

    if strict_filter:
        descriptions = descriptions.filter(protocol_id=protocol_id)

    if name_filter:
        descriptions = descriptions.filter(name__in=name_filter)

    if expression_filter:
        descriptions = descriptions.filter_by_expressions(expression_filter)

    table = DescriptionTable(descriptions)
    RequestConfig(request, paginate={"per_page": 10}).configure(table)
    context.update(
        {
            "table": table,
            "form_protocol": form_protocol,
            "formset": formset,
            "form_name": form_name,
            "form_strict": form_strict,
        }
    )

    context.update(generate_breadcrumbs(request, Description))

    if request.headers.get("HX-Request") == "true":
        rendered_block = render_block_to_string(
            template_name,
            "description_table",
            context,
            request,
        )
        return HttpResponse(rendered_block)

    return TemplateResponse(request, template_name, context)


def update_filter(request, **kwargs):
    for key, value in kwargs.items():
        request.session["description_filter"][key] = value
    request.session.modified = True


@require_POST
def description_filter_update_expression(request):
    description_filter = init_description_filter(request)
    protocol_id = description_filter["protocol"]
    traits = Trait.objects.filter(protocol=protocol_id).with_states()
    formset = ExpressionFilterFormSet(request.POST, traits=traits)
    if formset.is_valid():
        expressions = formset.get_expression_ids()  # type: ignore[attr-defined]
        update_filter(request, expressions=expressions)
    return redirect(reverse("describe:description_list"))


@require_POST
def description_filter_update_name(request):
    form = DescriptionFilterForm(request.POST)
    if form.is_valid():
        names = form.cleaned_data["name"]
        update_filter(request, name=names)
    return redirect(reverse("describe:description_list"))


@require_POST
def description_filter_update_strict(request):
    form = ProtocolStrictSearchForm(request.POST)
    if form.is_valid():
        strict = form.cleaned_data["strict"]
        update_filter(request, strict=strict)
    return redirect(reverse("describe:description_list"))


def description_form(request):
    protocol_id = request.GET.get("protocol", None)
    if not protocol_id:
        return HttpResponseBadRequest()

    template_name = "describe/description_list.html"

    update_filter(
        request,
        expressions={},
        protocol=protocol_id,
    )

    traits = Trait.objects.filter(protocol=protocol_id).prefetch_related("states").order_by("numeric_id")
    formset = ExpressionFilterFormSet(traits=traits)

    context = {"formset": formset}

    rendered_block = render_block_to_string(
        template_name,
        block_name="expression_filter",
        context=context,
        request=request,
    )
    return HttpResponse(content=rendered_block)


def make_filter_from_expressions(expressions):
    filter_expression = defaultdict(list)
    for e in expressions:
        filter_expression[e.state.trait.pk].append(e.state.pk)
    return list(filter_expression.values())


def description_find_similar(request):
    """Populate filter form with similar traits based on a reference description."""

    template_name = "describe/description_list.html"

    description_id = request.GET.get("description_id")
    description = get_object_or_404(Description, pk=description_id)

    form_protocol_filter, protocol = get_protocol_form(request, description.protocol)
    form_strict_search, filter_strict = get_strict_search_form(request)

    traits = protocol.with_traits_and_states()
    expressions = get_description_asterisked_expression(description_id)

    filter_expression = make_filter_from_expressions(expressions)

    formset_expression = ExpressionFilterFormSet(expressions=expressions, traits=traits)

    form_description_filter = description_form(request)

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
