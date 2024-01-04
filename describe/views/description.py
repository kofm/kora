"""
Description Views
List, Detail, Update, Create, Delete
"""

from django.db.models.functions import Lower
from django_tables2 import RequestConfig

from describe.filters import DescriptionFilterByName
from describe.forms import (
    DescriptionFilterFormSet,
    DescriptionForm,
    DescriptionImportForm,
    ExpressionFormSet,
    ExpressionUpdateForm,
    ProtocolForm,
)
from describe.models import Description, Expression, Protocol, State, Trait
from describe.tables import DescriptionTable
from describe.utils import _filter_descriptions, delete_get_param, merge_unique
from django.db.models import Q, CharField
from django.db.models.expressions import F
from django.forms.models import model_to_dict
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect
from django.template.response import TemplateResponse
from django.urls import reverse
from django.urls.base import reverse_lazy
from django.views.decorators.http import require_POST
from django.views.generic import DetailView
from django.views.generic.edit import DeleteView
from describe.views.protocol import NavActiveDescribe
from frontpage.decorators import nav_active
from register.models import PlantVariety

CharField.register_lookup(Lower)

nav_describe = nav_active("nav_describe")


@nav_describe
def description_list(request):
    """List of Descriptions
    Filter descriptions by state of expression(s) according to the selected reference
    protocol
    """
    context = dict()

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
        queryset = Description.objects.filter_by_expression(request.session.get("description_filter"))
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
    description_table = DescriptionTable(description_filter_by_name.qs)
    RequestConfig(request, paginate={"per_page": 15}).configure(description_table)

    # Check if the current request is an htmx request, then render only the
    # relevant part of the page; otherwise return the full page
    if request.htmx:
        base_template = "describe/description_list_partial.html"
    else:
        base_template = "describe/description_list_base.html"

    description_favourites_ids = request.session.get("description_favourites", None)
    if description_favourites_ids:
        description_favourites = Description.objects.filter(pk__in=description_favourites_ids)
        context.update({"description_favourites": description_favourites})
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
    try:
        del request.session["description_filter"]
    except KeyError:
        pass


def description_list_reset(request):
    reset_description_filter(request)
    return redirect(reverse_lazy("describe:description-list"))


def description_find_similar(request):
    """
    This view gets a description_id as input and set the description filter
    with the grouping characteristics of the description.
    """
    description_id = request.GET.get("description_id", None)

    if description_id:
        description_filter = Expression.objects.filter(
            description__pk=description_id, state__trait__grouping=True
        ).values(trait=F("state__trait"), states=F("state"))
        # Transform the filter to ease querying with __in
        request.session["description_filter"] = [
            {
                "trait": filter["trait"],
                "state": [
                    filter["states"],
                ],
            }
            for filter in list(description_filter)
        ]
    return redirect(reverse_lazy("describe:description-list"))


def description_favourite_add(request):
    description_id = request.GET.get("description_id", None)
    if description_id:
        if "description_favourites" not in request.session:
            request.session["description_favourites"] = list()
        request.session["description_favourites"].append(description_id)
        request.session.modified = True
    description_favourites = Description.objects.filter(pk__in=request.session["description_favourites"])
    return TemplateResponse(
        request,
        "describe/partials/description_favourites.html",
        {"description_favourites": description_favourites},
    )


def description_favourite_clear(request):
    if "description_favourites" in request.session:
        del request.session["description_favourites"]
    return HttpResponse("")


@nav_describe
def description_compare(request):
    context = {}
    description_favourites_ids = request.session.get("description_favourites", None)
    if description_favourites_ids:
        descriptions = Description.objects.filter(pk__in=description_favourites_ids)
        protocols = Protocol.objects.filter(descriptions__in=descriptions).distinct()

        comparison_table = [{"protocol": protocol.name} for protocol in protocols]
        comparison_table_header = [f"{description.variety.name} - {description.name}" for description in descriptions]

        for index, protocol in enumerate(protocols):
            comparison_table[index]["rows"] = []
            for trait in protocol.traits.all():
                row = [
                    f"{trait.numeric_id}. {trait.description}",
                ]
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
                equal = all([id == expression_ids[0] for id in expression_ids])
                comparison_table[index]["rows"].append({"values": row, "equal": equal})
        context.update({"comparison_table_header": comparison_table_header})
        context.update({"comparison_table": comparison_table})
        return TemplateResponse(request, "describe/description_compare.html", context)
    else:
        return reverse("describe:description-list")


class DescriptionDetail(NavActiveDescribe, DetailView):
    model = Description
    context_object_name = "description"


@nav_describe
def description_update(request, pk):
    # Get the description object
    description = get_object_or_404(Description, pk=pk)
    # Collect all the existing expressions
    exist_expr = description.expressions.all()
    # This is the forms list
    forms = []
    if request.method == "POST":
        form_has_errors = False
        for expr_id, state_id in zip(request.POST.getlist("id"), request.POST.getlist("state")):
            if state_id:
                form = ExpressionUpdateForm({"id": expr_id, "state": state_id})
                if form.is_valid():
                    if exist_expr.filter(pk=form.cleaned_data["id"]).exists() and not exist_expr.filter(
                        state=form.cleaned_data["state"]
                    ):
                        exist_expr.filter(pk=form.cleaned_data["id"]).update(state=form.cleaned_data["state"])
                    else:
                        if not exist_expr.filter(state=form.cleaned_data["state"]):
                            new_expression = Expression()
                            new_expression.state = form.cleaned_data["state"]
                            new_expression.description = description
                            new_expression.save()
                else:
                    form_has_errors = True
            else:
                if expr_id:
                    exist_expr.filter(pk=expr_id).delete()
        if not form_has_errors:
            return HttpResponseRedirect(reverse("describe:description-detail", args=(description.id,)))

    for trait in description.available_traits:
        if exist_expr.filter(state__trait=trait).exists():
            e = exist_expr.get(state__trait=trait)
            form = ExpressionUpdateForm(model_to_dict(e))
        else:
            form = ExpressionUpdateForm()
        form.fields["state"].queryset = State.objects.filter(trait=trait)
        forms.append(form)
    formset = zip(forms, description.available_traits)
    return TemplateResponse(
        request,
        "describe/description_manage.html",
        context={"description": description, "formset": formset},
    )


@nav_describe
def description_update_metadata(request, pk):

    description = get_object_or_404(Description, pk=pk)
    form = DescriptionForm(request.POST or None, instance=description)

    if form.is_valid():
        description = form.save()
        return HttpResponseRedirect(
            reverse(
                "describe:description-detail",
                args=(description.pk,),
            )
        )

    sources = Description.get_existing_sources()
    return TemplateResponse(
        request,
        "describe/description_form.html",
        {
            "form": form,
            "sources": [{"value": source, "text": source} for source in sources],
            "description": description,
            "variety": description.variety,
            "updating": True,
        },
    )


@nav_describe
def description_create(request):
    context = {}

    form = DescriptionForm(request.POST or None)
    if form.is_valid():
        description = form.save()
        return HttpResponseRedirect(
            reverse(
                "describe:description-detail",
                args=(description.pk,),
            )
        )

    variety_id = request.GET.get("variety_id", None)
    if variety_id:
        variety = get_object_or_404(PlantVariety, pk=variety_id)
        form.initial["variety"] = variety
        context["variety"] = variety

    sources = Description.get_existing_sources()

    context["form"] = form
    context["sources"] = [{"value": source, "text": source} for source in sources]

    return TemplateResponse(request, "describe/description_form.html", context)


class DescriptionDeleteView(NavActiveDescribe, DeleteView):
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


def description_import(request):
    """
    This view is responsible for receiving the CSV file and creating the
    formset for user to review the data being imported.
    DescriptionImportForm handles the csv file validation and returns a
    dictionary that can be used to create the formset. It also returns a list
    of validation error for the cases in which the supplied variety_name
    returns multiple PlantVariety objects, and a data object containing all the
    Trait/State objects available for the selected Protocol that are needed to
    init the ExpressionFormSet.
    """
    form = DescriptionImportForm(request.POST or None, request.FILES or None)
    print("Hello")
    if form.is_valid():
        protocol = form.cleaned_data["protocol"]
        # This is needed in the view to populate the TomSelect inputs
        varieties = PlantVariety.objects.get_by_species_values_list(plantspecies=protocol.plantspecies)
        formset_data, multiple_objects_returned_errors, traits_states_list = form.save()
        formset = ExpressionFormSet(
            formset_data,
            form_kwargs={
                "traits": traits_states_list,
            },
        )
        for error in multiple_objects_returned_errors:
            formset[error["form"]].add_error(
                "variety",
                f"There are multiple varieties named '{error['variety_name']}'. \
                Please select one or create a new one",
            )
        return TemplateResponse(
            request,
            "describe/description_import_confirm.html",
            {"formset": formset, "varieties": varieties, "protocol": protocol},
        )
    return TemplateResponse(request, "describe/description_import.html", {"form": form})


@require_POST
def description_import_confirm(request, protocol_id):
    # Init the formset
    protocol = get_object_or_404(Protocol, pk=protocol_id)
    traits_states_list = protocol.traits_states_list()
    formset = ExpressionFormSet(
        request.POST,
        form_kwargs={
            "traits": traits_states_list,
        },
    )

    if formset.is_valid():
        for form in formset:
            form.save()
        return HttpResponseRedirect(reverse("describe:description-list"))

    # This is needed to populate the TomSelect inputs
    varieties = PlantVariety.objects.get_by_species_values_list(plantspecies=protocol.plantspecies)
    return TemplateResponse(
        request,
        "describe/description_import_confirm.html",
        {"formset": formset, "varieties": varieties, "protocol": protocol},
    )
