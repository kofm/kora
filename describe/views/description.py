"""Description Views.

List, Detail, Update, Create, Delete
"""

from collections import defaultdict

from django.contrib.auth.decorators import login_required
from django.db.models import CharField
from django.db.models.functions import Lower
from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect
from django.template.response import TemplateResponse
from django.urls import reverse, reverse_lazy
from django.utils.http import urlencode
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
from describe.models import Description, Expression, Protocol, Trait, Workspace, WorkspaceElement
from describe.tables import DescriptionTable
from describe.views.protocol import NavDescribeActiveContext
from describe.views.utils import (
    init_description_filter,
    make_descriptions_dict,
    make_species_descriptions_dict,
    make_species_protocols_dict,
    make_traits_expressions_dict,
    process_description_filter,
    render_export_file_to_response,
    reset_description_filter,
    update_description_filter,
)
from frontpage.views_decorators import nav_active
from register.models import PlantVariety

CharField.register_lookup(Lower)

nav_describe = nav_active("nav_describe")


@nav_describe
def description_list(request):
    reset = request.GET.get("reset") != "false"
    if not request.headers.get("HX-Request") == "true" and reset:
        reset_description_filter(request)

    description_filter = init_description_filter(request)
    protocol_id = description_filter["protocol"]

    if request.method == "POST":
        if "name" in request.POST:
            form = DescriptionFilterForm(request.POST)
            if form.is_valid():
                names = form.cleaned_data["name"]
                update_description_filter(request, name=names)
        if "strict_changed" in request.POST:
            form = ProtocolStrictSearchForm(request.POST)
            if form.is_valid():
                strict = form.cleaned_data["strict"]
                update_description_filter(request, strict=strict)
        if "form-TOTAL_FORMS" in request.POST:
            traits = Trait.objects.filter(protocol=protocol_id).with_states()
            formset = ExpressionFilterFormSet(request.POST, traits=traits)
            if formset.is_valid():
                expressions = formset.get_expression_ids()  # type: ignore[attr-defined]
                update_description_filter(request, expressions=expressions)
        return HttpResponseRedirect("")

    template_name = "describe/description_list.html"
    context = {}

    descriptions = process_description_filter(Description.objects.with_expressions(), description_filter)

    if request.GET.get("export") == "true":
        return render_export_file_to_response(
            protocol_id,
            description_filter["expressions"],
            descriptions,
        )

    table = DescriptionTable(descriptions)
    RequestConfig(request, paginate={"per_page": 10}).configure(table)

    if request.headers.get("HX-Request") == "true":
        table_block = render_block_to_string(
            template_name,
            "description_table",
            {"table": table},
            request,
        )
        return HttpResponse(table_block)

    traits = Trait.objects.filter(protocol=protocol_id).with_states()
    context["form_protocol"] = ProtocolForm(initial={"protocol": protocol_id})
    context["form_strict"] = ProtocolStrictSearchForm(initial={"strict": description_filter["strict"]})
    context["form_name"] = DescriptionFilterForm(initial={"name": description_filter["name"]})
    context["formset"] = ExpressionFilterFormSet(traits=traits, expressions=description_filter["expressions"])
    context["table"] = table
    context.update(generate_breadcrumbs(request, Description))

    return TemplateResponse(request, template_name, context)


def description_form(request):
    protocol_id = request.GET.get("protocol", None)
    if not protocol_id:
        return HttpResponseBadRequest()

    template_name = "describe/description_list.html"

    update_description_filter(request, expressions={}, protocol=protocol_id)

    traits = Trait.objects.filter(protocol=protocol_id).prefetch_related("states").order_by("numeric_id")
    formset = ExpressionFilterFormSet(traits=traits)

    context = {"formset": formset}

    rendered_block = render_block_to_string(
        template_name,
        block_name="expression_filter",
        context=context,
        request=request,
    )
    return HttpResponse(rendered_block)


def description_find_similar(request):
    """Populate filter form with similar traits based on a reference description."""

    template_name = "describe/description_list.html"

    description_id = request.GET.get("description_id")
    description = get_object_or_404(Description, pk=description_id)

    protocol_id = description.protocol.pk

    expressions = Expression.objects.prefetch_related("state__trait").filter(
        description=description_id, state__trait__grouping=True
    )

    filter_expression = defaultdict(list)
    for expression in expressions:
        filter_expression[str(expression.state.trait.pk)].append(expression.state.pk)

    update_description_filter(request, expressions=dict(filter_expression), protocol=protocol_id)

    if not request.headers.get("HX-Request") == "true":
        url = reverse("describe:description_list")
        query_string = urlencode({"reset": "false"})
        return redirect(f"{url}?{query_string}")

    traits = Trait.objects.filter(protocol=protocol_id).prefetch_related("states").order_by("numeric_id")
    form = ProtocolForm(initial={"protocol": protocol_id})
    formset = ExpressionFilterFormSet(traits=traits, expressions=dict(filter_expression))

    expression_block = render_block_to_string(
        template_name,
        block_name="expression_filter",
        context={"formset": formset},
        request=request,
    )
    protocol_block = render_block_to_string(
        template_name,
        block_name="protocol_filter",
        context={"form_protocol": form},
        request=request,
    )

    return HttpResponse(expression_block + protocol_block)


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
