from collections import defaultdict
from datetime import datetime
from itertools import groupby

from django.db.models import QuerySet
from django.http import HttpRequest, HttpResponse

from describe.models import Description, Protocol, State
from frontpage.views_decorators import is_htmx


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


def render_header(string):
    return [
        "",
        "==========================",
        string,
        "==========================",
        "",
    ]


def render_filter_expression_to_text(filter_expression):
    states = [state for _, states in filter_expression.items() for state in states]
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


def render_search_info(protocol_id):
    protocol = Protocol.objects.get(id=protocol_id)
    return render_header("Description Search") + [f"Protocol: {protocol.name}"]


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
    reset = request.GET.get("reset") != "false"
    if not is_htmx(request) and reset:
        reset_description_filter(request)

    if "description_filter" not in request.session:
        protocol = Protocol.objects.first()
        request.session["description_filter"] = {
            "protocol": protocol.pk if protocol else None,
            "strict": False,
            "name": [],
            "expressions": {},
        }
    return request.session["description_filter"]


def reset_description_filter(request):
    if "description_filter" in request.session:
        del request.session["description_filter"]


def update_description_filter(request, **kwargs):
    for key, value in kwargs.items():
        request.session["description_filter"][key] = value
    request.session.modified = True


def process_description_filter(descriptions: QuerySet[Description], description_filter: dict) -> QuerySet[Description]:
    protocol_id = description_filter["protocol"]
    expression_filter = description_filter["expressions"]
    name_filter = description_filter["name"]
    strict_filter = description_filter["strict"]

    if strict_filter:
        descriptions = descriptions.filter(protocol_id=protocol_id)

    if name_filter:
        descriptions = descriptions.filter(name__in=name_filter)

    if expression_filter:
        descriptions = descriptions.filter_by_expressions(expression_filter)

    return descriptions
