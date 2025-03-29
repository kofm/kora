from collections import defaultdict
from datetime import datetime
from itertools import groupby

from django.db.models import QuerySet
from django.forms import BaseFormSet
from django.http import HttpRequest, HttpResponse
from django.urls import reverse

from describe.forms import (
    DescriptionFilterForm,
    ExpressionFilterFormSet,
    ProtocolForm,
    ProtocolStrictSearchForm,
)
from describe.models import Expression, Protocol, State
from register.filters import filter_name_generic


def join_description_expressions(
    states_dict: dict[int, str],
    descriptions: dict[tuple, list],
) -> list[list[tuple]]:
    descriptions_list = []
    for key in descriptions:
        expression_filter = filter(lambda x: x[0] in states_dict, descriptions[key])
        expression_found = [(states_dict[expression_id], note) for expression_id, note in expression_filter]
        descriptions_list.append(expression_found)
    return descriptions_list


def list_elems_equal(expressions: list[list]) -> bool:
    non_empty_items = [expr for expr in expressions if expr]
    if non_empty_items:
        comparable_items = [tuple(sorted(item)) for item in non_empty_items]
        return len(set(comparable_items)) == 1
    return True


def make_species_descriptions_dict(descriptions: QuerySet) -> dict[tuple, dict[tuple, list]]:
    result: dict[tuple, dict[tuple, list]] = {}

    descriptions_dict = descriptions.annotated()  # type: ignore[attr-defined]

    grouped_species = groupby(
        descriptions_dict,
        lambda x: (x["species_id"], x["species_name"]),
    )

    for species_key, description_data in grouped_species:
        result[species_key] = make_descriptions_dict(description_data)

    return result


def make_descriptions_dict(description_values):
    result = {}
    grouped_descriptions = groupby(
        description_values,
        lambda x: (x["variety__id"], x["variety__name"], x["name"]),
    )

    for description_key, expressions in grouped_descriptions:
        result[description_key] = [(expression["state_id"], expression["note"]) for expression in expressions]

    return result


def make_species_protocols_dict(
    protocols: QuerySet,
    descriptions_dict: dict[tuple, dict[tuple, list]],
) -> dict[tuple, dict]:
    res: dict[tuple, dict] = {}
    for protocol in protocols:
        species = protocol.plantspecies
        species_key = (
            species.pk,
            species.common_name,
        )  # This should match the species key generated in make_descriptions_dict

        if species_key not in res:
            res[species_key] = {}
            res[species_key]["descriptions"] = list(descriptions_dict[species_key].keys())
            res[species_key]["protocols"] = {}

        protocol_key = protocol.name
        traits = protocol.traits.all()

        res[species_key]["protocols"][protocol_key] = make_traits_expressions_dict(
            traits,
            descriptions_dict[species_key],
        )
    return res


def make_traits_expressions_dict(
    traits: QuerySet,
    descriptions_dict: dict[tuple, list],
) -> dict[tuple, dict]:
    res: dict[tuple, dict] = {}
    for trait in traits:
        states = trait.states.all()
        states_dict = {state.pk: f"{state.numeric_id}. {state.description}" for state in states}

        descriptions_expression_str = join_description_expressions(states_dict, descriptions_dict)
        trait_key = (trait.numeric_id, trait.description, trait.grouping)
        res[trait_key] = {}
        res[trait_key]["expressions"] = descriptions_expression_str
        res[trait_key]["all_equal"] = list_elems_equal(descriptions_expression_str)

    return res


def get_description_form(request: HttpRequest):
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


def get_protocol_form(request: HttpRequest) -> tuple[ProtocolForm, Protocol]:
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


def get_strict_search_form(request: HttpRequest) -> tuple[ProtocolStrictSearchForm, bool]:
    result = False
    form = ProtocolStrictSearchForm()
    if request.method == "POST":
        form = ProtocolStrictSearchForm(request.POST)
        if form.is_valid():
            result = form.cleaned_data.get("strict")  # type: ignore
    return (form, result)


def get_expression_filter(request: HttpRequest, protocol: Protocol) -> tuple[BaseFormSet, list]:
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


def get_description_asterisked_expression(description_id):
    return Expression.objects.prefetch_related("state__trait").filter(
        description=description_id, state__trait__grouping=True
    )


def render_header(string):
    return [
        "",
        "==========================",
        string,
        "==========================",
        "",
    ]


def render_filter_expression_to_text(filter_expression):
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

    text = render_header(f"Expression Filters ({len(filter_expression)})")
    for trait, states in output.items():
        text.append(trait)

        for state in states:
            text.append(f"    {state}")
    return text


def render_search_info(protocol):
    return render_header("Description Search") + [
        f"Protocol: {protocol.name}",
    ]


def render_description_list(descriptions):
    header = render_header(f"Results ({descriptions.count()}):")
    body = [f"- {description}" for description in descriptions]
    return header + body


def render_export_file_to_response(protocol, filter_expression, descriptions):
    text = (
        render_search_info(protocol)
        + render_filter_expression_to_text(filter_expression)
        + render_description_list(descriptions)
    )
    curtime = datetime.today().strftime("%Y%m%d%H%M%S")
    filename = f"description_filter_{curtime}.txt"
    response = HttpResponse("\n".join(text), content_type="text/plain")
    response["Content-Disposition"] = f"attachment; filename={filename}"
    return response


def init_description_filter(request: HttpRequest):
    if "description_filter" not in request.session:
        request.session["description_filter"] = {
            "protocol": Protocol.objects.most_used().pk,
            "strict": False,
            "name": [],
            "expressions": {},
        }
    return request.session["description_filter"]
