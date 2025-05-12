"""Description Views.

List, Detail, Update, Create, Delete
"""

from collections import defaultdict

from django.contrib import messages
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.db.models import CharField, Q
from django.db.models.functions import Lower
from django.http import HttpResponseBadRequest, HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect
from django.template.response import TemplateResponse
from django.urls import reverse, reverse_lazy
from django.utils.http import urlencode
from django.views.generic import DeleteView
from django_tables2 import RequestConfig

from breadcrumbs.generic import DeleteBreadcrumbsMixin
from breadcrumbs.utils import add_parent_breadcrumbs, add_plantvariety_breadcrumbs, generate_breadcrumbs
from describe.forms import (
    DescriptionForm,
    DescriptionNameForm,
    DescriptionUpdateForm,
    DescriptionVarietyForm,
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
    update_description_filter,
)
from frontpage.views_decorators import (
    htmx_render_blocks,
    is_htmx,
    make_get_request,
    nav_active,
)
from register.filters import filter_name_generic
from register.models import PlantVariety

CharField.register_lookup(Lower)

nav_describe = nav_active("nav_describe")


@nav_describe
@htmx_render_blocks(["description_table"])
def description_list(request):
    return _description_list(request)


def _description_list(request):
    description_filter = init_description_filter(request)
    protocol_id = description_filter["protocol"]

    if request.method == "POST":
        if "name_form" in request.POST:
            if "name" in request.POST:
                form = DescriptionNameForm(request.POST)
                if form.is_valid():
                    names = form.cleaned_data["name"]
                    update_description_filter(request, name=names)
            else:
                update_description_filter(request, name=[])
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
        if is_htmx(request):
            return _description_list(make_get_request(request))
        return HttpResponseRedirect("")

    context = {}

    descriptions = process_description_filter(Description.objects.with_expressions(), description_filter)

    if "variety" in request.GET:
        form = DescriptionVarietyForm(request.GET)
        if form.is_valid():
            variety_name = form.cleaned_data["variety"]
            descriptions = filter_name_generic(descriptions, "variety__name", variety_name)

    if "export" in request.GET:
        return render_export_file_to_response(
            protocol_id,
            description_filter["expressions"],
            descriptions,
        )

    table = DescriptionTable(descriptions)
    RequestConfig(request).configure(table)

    traits = Trait.objects.filter(protocol=protocol_id).with_states()
    context["form_variety"] = DescriptionVarietyForm()
    context["form_protocol"] = ProtocolForm(initial={"protocol": protocol_id})
    context["form_strict"] = ProtocolStrictSearchForm(initial={"strict": description_filter["strict"]})
    context["form_name"] = DescriptionNameForm(initial={"name": description_filter["name"]})
    context["formset"] = ExpressionFilterFormSet(traits=traits, expressions=description_filter["expressions"])
    context["table"] = table
    context.update(generate_breadcrumbs(request, Description))

    return TemplateResponse(request, "describe/description_list.html", context)


@htmx_render_blocks(["expression_filter"])
@permission_required("describe.add_description", raise_exception=True)
def description_form(request):
    protocol_id = request.GET.get("protocol", None)
    if not protocol_id:
        return HttpResponseBadRequest()
    update_description_filter(request, expressions={}, protocol=protocol_id)
    traits = Trait.objects.filter(protocol=protocol_id).prefetch_related("states").order_by("numeric_id")
    formset = ExpressionFilterFormSet(traits=traits)
    return TemplateResponse(request, "describe/description_list.html", {"formset": formset})


@htmx_render_blocks(["expression_filter", "protocol_filter"])
def description_find_similar(request):
    """Populate filter form with similar traits based on a reference description."""
    description_id = request.GET.get("description_id")

    if not description_id:
        return redirect(reverse("describe:description_list"))

    description = get_object_or_404(Description, pk=description_id)
    protocol_id = description.protocol.pk
    expressions = Expression.objects.prefetch_related("state__trait").filter(
        description=description_id, state__trait__grouping=True
    )
    if not expressions:
        messages.warning(request, "No asterisked expressions available for this variety.")
    filter_expression = defaultdict(list)
    for expression in expressions:
        filter_expression[str(expression.state.trait.pk)].append(expression.state.pk)
    update_description_filter(request, expressions=dict(filter_expression), protocol=protocol_id)

    if not is_htmx(request):
        url = reverse("describe:description_list")
        query_string = urlencode({"reset": "false"})
        return redirect(f"{url}?{query_string}")

    traits = Trait.objects.filter(protocol=protocol_id).prefetch_related("states").order_by("numeric_id")
    form = ProtocolForm(initial={"protocol": protocol_id})
    formset = ExpressionFilterFormSet(traits=traits, expressions=dict(filter_expression))

    return TemplateResponse(request, "describe/description_list.html", {"form_protocol": form, "formset": formset})


@nav_describe
@login_required
def description_compare(request):
    wsp = Workspace.objects.filter(user=request.user, is_active=True).first()
    if not wsp:
        return redirect(reverse("describe:description_list"))

    elems = WorkspaceElement.objects.select_related("description__variety__species").filter(workspace=wsp)
    if not elems:
        return redirect(reverse("describe:description_list"))

    # Get all the available Descriptions for any of the Variety-Name
    # combinations present in the workspace.
    # This includes descriptions from other protocols, too.
    pairs = elems.values_list("description__variety_id", "description__name").distinct()
    query = Q()
    for variety_id, name in pairs:
        query |= Q(variety_id=variety_id, name=name)
    descriptions = Description.objects.filter(query)

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
@permission_required("describe.change_description", raise_exception=True)
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
@htmx_render_blocks(["protocol_form"])
@permission_required("describe.add_description", raise_exception=True)
def description_create(request):
    context = {}

    if request.method == "POST":
        form = DescriptionForm(request.POST)
        if form.is_valid():
            description = form.save()
            return redirect(reverse("describe:description_expression_update", args=(description.pk,)))
    else:
        form = DescriptionForm()
        form.fields["variety"].queryset = PlantVariety.objects.all()[0:10]
        form.fields["protocol"].disabled = True

    variety_id = request.GET.get("variety", None)
    if variety_id:
        variety = get_object_or_404(PlantVariety, pk=variety_id)
        form.initial["variety"] = variety
        form.fields["protocol"].queryset = Protocol.objects.filter(plantspecies=variety.species_id)
        form.fields["protocol"].disabled = False
        context["variety"] = variety
    context["form"] = form
    context["model_name"] = "Description"
    context.update(generate_breadcrumbs(request, Description))

    return TemplateResponse(request, "describe/description_create.html", context)


class DescriptionDeleteView(PermissionRequiredMixin, DeleteBreadcrumbsMixin, NavDescribeActiveContext, DeleteView):
    model = Description
    success_url = reverse_lazy("describe:description_list")
    permission_required = ["describe.delete_description"]


@permission_required("describe.change_expression", raise_exception=True)
@htmx_render_blocks(["header", "description_form"])
def description_expression_update(request, pk):
    context = {}
    description = Description.objects.select_related("variety__species", "protocol__plantspecies").get(pk=pk)
    if request.method == "POST":
        undo = {"variety": description.variety_id, "name": description.name}
        description_form = DescriptionUpdateForm(request.POST, instance=description)
        if description_form.is_valid():
            description_form.save()
            if "undo" not in request.POST:
                context.update({"undo": undo})
    else:
        description_form = DescriptionUpdateForm(instance=description)

    context.update({"description": description, "form": description_form})

    if not is_htmx(request):
        traits = Trait.objects.prefetch_related("states").filter(protocol=description.protocol_id)
        state_choices = {t.pk: [(s.pk, str(s)) for s in t.states.all()] for t in traits}
        formset = []
        expressions_dict = defaultdict(list)
        for e in Expression.objects.prefetch_related("state__trait").filter(description=description):
            expressions_dict[e.state.trait.pk].append(e)

        for trait in traits:
            expressions = expressions_dict[trait.pk]
            forms = []
            if expressions:
                for expression in expressions:
                    form = ExpressionForm(instance=expression, auto_id=False)
                    form.fields["state"].choices = state_choices[trait.pk]
                    forms.append(form)
            formset.append({"trait": trait, "forms": forms})
        context["formset"] = formset

    crumbs = generate_breadcrumbs(request, Description, description)
    crumbs = add_parent_breadcrumbs(crumbs, description.variety)
    context.update(crumbs)
    return TemplateResponse(request, "describe/description_expression_update.html", context)
