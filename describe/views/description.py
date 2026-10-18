"""Description Views.

List, Detail, Update, Create, Delete
"""

from collections import defaultdict

from django.contrib import messages
from django.contrib.auth.decorators import login_required, permission_required, user_passes_test
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.db import transaction
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
    DescriptionDuplicateForm,
    DescriptionFilterLabelForm,
    DescriptionForm,
    DescriptionLabelForm,
    DescriptionUpdateForm,
    DescriptionVarietyForm,
    ExpressionFilterFormSet,
    ExpressionForm,
    ProtocolForm,
    ProtocolStrictSearchForm,
)
from describe.models import Description, DescriptionLabel, Expression, Protocol, Trait, Workspace, WorkspaceElement
from describe.tables import DescriptionTable
from describe.views.protocol import NavDescribeActiveContext
from describe.views.utils import (
    description_results,
    init_description_filter,
    make_descriptions_dict,
    make_species_descriptions_dict,
    make_species_protocols_dict,
    make_traits_expressions_dict,
    render_export_file_to_response,
    update_description_filter,
)
from frontpage.headers import DetailHeader, HeaderAction, ListHeader
from frontpage.utils.htmx import htmx_response_redirect
from frontpage.utils.models import copy_model_concrete_fields
from frontpage.views_decorators import (
    htmx_render_partial,
    is_htmx,
    make_get_request,
    nav_active,
    public_catalog_view,
)
from register.models import PlantVariety

CharField.register_lookup(Lower)

nav_describe = nav_active("nav_describe")


@nav_describe
@public_catalog_view("describe.view_description")
@htmx_render_partial("description_table")
def description_list(request):
    return _description_list(request)


def _description_list(request):
    description_filter = init_description_filter(request)
    protocol_id = description_filter["protocol"]

    if request.method == "POST":
        if "label_form" in request.POST:
            if "labels" in request.POST:
                form = DescriptionFilterLabelForm(request.POST)
                if form.is_valid():
                    labels = form.cleaned_data["labels"]
                    update_description_filter(request, label=list(labels.values_list("pk", flat=True)))
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

    descriptions, filtered, variety = description_results(
        Description.objects.with_expressions().select_related("label"), description_filter, request.GET
    )

    if "export" in request.GET:
        return render_export_file_to_response(
            protocol_id,
            description_filter["label"],
            description_filter["expressions"],
            descriptions,
        )

    table = DescriptionTable(descriptions)
    RequestConfig(request).configure(table)

    traits = Trait.objects.filter(protocol=protocol_id).with_states()
    context["form_variety"] = DescriptionVarietyForm()
    context["form_protocol"] = ProtocolForm(initial={"protocol": protocol_id})
    context["form_strict"] = ProtocolStrictSearchForm(initial={"strict": description_filter["strict"]})
    context["form_label"] = DescriptionFilterLabelForm(initial={"label": description_filter["label"]})
    context["formset"] = ExpressionFilterFormSet(traits=traits, expressions=description_filter["expressions"])
    context["table"] = table
    context["results_filtered"] = filtered
    context["bulk_add_url"] = (
        reverse("describe:workspace_elements_add_results")
        + "?"
        + urlencode({"variety": variety, "sort": str(table.order_by or "")})
    )
    context["header"] = ListHeader(
        request,
        Description,
        modal=True,
        actions=[HeaderAction("Configure", Description.get_configure_url(), "describe.add_description", modal=True)],
    )
    context.update(generate_breadcrumbs(request, Description))

    return TemplateResponse(request, "describe/description_list.html", context)


@htmx_render_partial("expression_filter")
@permission_required("describe.add_description", raise_exception=True)
def description_form(request):
    protocol_id = request.GET.get("protocol", None)
    if not protocol_id:
        return HttpResponseBadRequest()
    update_description_filter(request, expressions={}, protocol=protocol_id)
    traits = Trait.objects.filter(protocol=protocol_id).prefetch_related("states").order_by("numeric_id")
    formset = ExpressionFilterFormSet(traits=traits)
    return TemplateResponse(
        request,
        "describe/description_list.html",
        {
            "formset": formset,
            "header": ListHeader(
                request,
                Description,
                modal=True,
                actions=[
                    HeaderAction("Configure", Description.get_configure_url(), "describe.add_description", modal=True),
                ],
            ),
        },
    )


@htmx_render_partial("similar_filters")
def description_find_similar(request):
    """Populate filter form with similar traits based on a reference description."""
    description_id = request.GET.get("description_id")

    if not description_id:
        return redirect(reverse("describe:description_list"))

    description = get_object_or_404(Description, pk=description_id)
    protocol_id = description.protocol.pk
    expressions = Expression.objects.select_related("state__trait").filter(
        description=description_id, state__trait__grouping=True
    )
    if not expressions:
        messages.warning(request, "No asterisked expressions available for this variety.")
    recorded_states = defaultdict(set)
    for expression in expressions:
        recorded_states[expression.state.trait_id].add(expression.state_id)

    traits = Trait.objects.filter(protocol=protocol_id).with_states()
    filter_expression = {}
    for trait in traits:
        selected = recorded_states.get(trait.pk)
        if not selected:
            continue
        states = list(trait.states.all())
        if trait.type_of_expression == Trait.TypeOfExpression.QUANTITATIVE:
            expanded = set(selected)
            for index, state in enumerate(states):
                if state.pk in selected:
                    expanded.update(neighbor.pk for neighbor in states[max(0, index - 1) : index + 2])
            selected = expanded
        filter_expression[str(trait.pk)] = [state.pk for state in states if state.pk in selected]
    update_description_filter(request, expressions=filter_expression, protocol=protocol_id)

    if not is_htmx(request):
        url = reverse("describe:description_list")
        query_string = urlencode({"reset": "false"})
        return redirect(f"{url}?{query_string}")

    form = ProtocolForm(initial={"protocol": protocol_id})
    formset = ExpressionFilterFormSet(traits=traits, expressions=filter_expression)

    return TemplateResponse(request, "describe/description_list.html", {"form_protocol": form, "formset": formset})


@nav_describe
@login_required
def description_compare(request):
    wsp = Workspace.objects.filter(user=request.user, is_active=True).first()
    template = "describe/description_compare.html"
    partial = request.GET.get("partial") if is_htmx(request) else None
    if partial not in {"header", "breadcrumbs", "comparison"}:
        partial = None
    context = {"workspace": wsp, "compare_table": {}}
    if partial != "comparison":
        context.update(generate_breadcrumbs(request, Workspace, wsp, skip_if_htmx=False))
    if partial in {"header", "breadcrumbs"}:
        return TemplateResponse(request, f"{template}#{partial}", context)

    # Keep the first occurrence of each variety/label pair in sidebar order.
    elems = (
        WorkspaceElement.objects.filter(workspace=wsp).order_by("order", "pk")
        if wsp else WorkspaceElement.objects.none()
    )
    pairs = list(dict.fromkeys(elems.values_list("description__variety_id", "description__label_id")))[:50]
    if not pairs:
        return TemplateResponse(request, f"{template}#{partial}" if partial else template, context)

    # Get all the available Descriptions for any of the Variety-Name
    # combinations present in the workspace.  This includes
    # descriptions from other protocols, too.
    query = Q()
    for variety_id, label in pairs:
        query |= Q(variety_id=variety_id, label=label)
    descriptions = Description.objects.filter(query)

    protocols = (
        Protocol.objects.select_related("plantspecies")
        .prefetch_related("traits__states")
        .filter(descriptions__in=descriptions)
    )

    descriptions_dictionary = make_species_descriptions_dict(descriptions)
    label_names = dict(DescriptionLabel.objects.filter(pk__in=[label for _, label in pairs]).values_list("pk", "name"))
    column_order = {(variety, label_names.get(label)): index for index, (variety, label) in enumerate(pairs)}
    for species, columns in descriptions_dictionary.items():
        descriptions_dictionary[species] = dict(
            sorted(columns.items(), key=lambda item: column_order[(item[0][0], item[0][2])])
        )
    compare_table = make_species_protocols_dict(protocols, descriptions_dictionary)
    labels = {label.name: label for label in DescriptionLabel.objects.filter(descriptions__in=descriptions).distinct()}
    for species_data in compare_table.values():
        species_data["descriptions"] = [
            {"variety": variety_name, "label": labels.get(label_name)}
            for _, variety_name, label_name in species_data["descriptions"]
        ]

    context["compare_table"] = compare_table
    return TemplateResponse(request, f"{template}#{partial}" if partial else template, context)


@public_catalog_view("describe.view_description")
def description_detail(request, pk):
    description = Description.objects.select_related("variety", "protocol").get(pk=pk)

    description_annotated = Description.objects.annotated().filter(pk=pk)
    description_dict = make_descriptions_dict(description_annotated)
    protocol = Protocol.objects.get(descriptions=pk)
    traits = protocol.with_traits_and_states()
    table = make_traits_expressions_dict(traits, description_dict)

    context = {
        "description": description,
        "table": table,
        "header": DetailHeader(request, description, title=description.variety),
    }
    breadcrumbs = generate_breadcrumbs(request, Description, description)
    breadcrumbs = add_plantvariety_breadcrumbs(breadcrumbs, description.variety)

    context.update(breadcrumbs)

    return TemplateResponse(request, "describe/description_detail.html", context)


@nav_describe
@permission_required("describe.add_description", raise_exception=True)
def description_create(request):
    context = {}

    if request.method == "POST":
        form = DescriptionForm(request.POST)
        if form.is_valid():
            description = form.save()
            url = reverse("describe:description_expression_update", args=(description.pk,))
            return htmx_response_redirect(url)
    else:
        variety_id = request.GET.get("variety", None)
        species_id = None
        if variety_id:
            variety = get_object_or_404(PlantVariety, pk=variety_id)
            species_id = variety.species_id
        form = DescriptionForm(
            initial={
                "variety": variety_id,
                "species": species_id,
            }
        )

    context["form"] = form
    context["object_to_create"] = "Description"
    context.update(generate_breadcrumbs(request, Description))

    return TemplateResponse(request, "describe/partials/description_create.html", context)


@permission_required("describe.add_description", raise_exception=True)
@transaction.atomic
def description_duplicate(request, pk):
    original = get_object_or_404(Description.objects.select_related("variety__species"), pk=pk)

    if request.method == "POST":
        form = DescriptionDuplicateForm(request.POST)
        if form.is_valid():
            new_description = form.save(commit=False)

            copy_model_concrete_fields(
                original,
                new_description,
                exclude={"name"},
            )
            new_description.save()

            Expression.objects.bulk_create(
                [
                    Expression(
                        description=new_description,
                        state=expr.state,
                        note=expr.note,
                    )
                    for expr in original.expressions.all()
                ]
            )
            messages.success(request, f"{original} duplicated successfully.")
            return htmx_response_redirect(new_description.get_absolute_url())
    else:
        form = DescriptionDuplicateForm()

    return TemplateResponse(request, "describe/description_duplicate.html", {"form": form, "instance": original})


class DescriptionDeleteView(PermissionRequiredMixin, DeleteBreadcrumbsMixin, NavDescribeActiveContext, DeleteView):
    model = Description
    success_url = reverse_lazy("describe:description_list")
    permission_required = ["describe.delete_description"]


@permission_required("describe.change_expression", raise_exception=True)
@htmx_render_partial("expression_update")
def description_expression_update(request, pk):
    context = {}
    description = Description.objects.select_related("variety__species", "protocol__plantspecies", "label").get(pk=pk)
    if request.method == "POST":
        description_form = DescriptionUpdateForm(request.POST, instance=description)
        if description_form.is_valid():
            description_form.save()
    else:
        description_form = DescriptionUpdateForm(instance=description)

    context.update({"description": description, "form": description_form})

    if not is_htmx(request):
        traits = Trait.objects.prefetch_related("states").filter(protocol=description.protocol_id)
        state_choices = {t.pk: [(s.pk, str(s)) for s in t.states.all()] for t in traits}
        formset = []
        expressions_dict = defaultdict(list)
        for e in Expression.objects.select_related("state__trait").filter(description=description):
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


@user_passes_test(lambda user: user.is_staff)
def description_configure(request):
    queryset = DescriptionLabel.objects.all()
    form = DescriptionLabelForm(request.POST or None)
    if form.is_valid():
        form.save()
        form = DescriptionLabelForm()
    context = {"labels": queryset, "form": form}
    return TemplateResponse(request, "describe/partials/description_configure.html", context)


@user_passes_test(lambda user: user.is_staff)
def description_label_update(request, pk):
    instance = get_object_or_404(DescriptionLabel, pk=pk)
    form = DescriptionLabelForm(request.POST or None, instance=instance)
    if form.is_valid():
        form.save()
        return redirect("describe:description_configure")
    context = {"description_label": instance, "form": form}
    return TemplateResponse(request, "frontpage/modal_form.html", context)
