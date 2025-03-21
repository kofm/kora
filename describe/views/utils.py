from itertools import groupby
from typing import Any

from django.db.models import F, QuerySet

from describe.models import Trait


def _state_to_str(state):
    return f"{state['states__numeric_id']}. {state['states__description']}"


def _get_protocol_traits_states_dict(protocols_queryset: QuerySet):
    queryset = (
        Trait.objects.filter(protocol_id__in=protocols_queryset)
        .select_related("protocol__species")
        .prefetch_related("states")
        .values(
            "protocol__name",
            "protocol__plantspecies__id",
            "protocol__plantspecies__common_name",
            "pk",
            "numeric_id",
            "description",
            "states__pk",
            "states__numeric_id",
            "states__description",
        )
        .order_by(
            "protocol__plantspecies__id",
            "protocol__name",
            "numeric_id",
            "states__numeric_id",
        )
    )

    result: dict[Any, Any] = {}
    grouped_species = groupby(
        queryset, lambda x: (x["protocol__plantspecies__id"], x["protocol__plantspecies__common_name"])
    )
    for species, protocols in grouped_species:
        result[species] = {}
        grouped_protocol = groupby(protocols, lambda x: x["protocol__name"])
        for protocol, traits in grouped_protocol:
            result[species][protocol] = {}
            for trait, states in groupby(traits, lambda x: (x["numeric_id"], x["description"])):
                states = {state["states__pk"]: _state_to_str(state) for state in list(states)}  # type: ignore[assignment]
                result[species][protocol][trait] = {"states": states}

    return result


def _get_descriptions_compare_dict(protocol_traits_states_dict, descriptions: QuerySet):
    for species in protocol_traits_states_dict.keys():
        descriptions_dict = (
            descriptions.select_related("variety__species")
            .prefetch_related("expressions")
            .filter(variety__species=species[0])
            .order_by(
                "variety__pk",
                "name",
            )
            .values(
                "variety__pk",
                "variety__name",
                "name",
                "expressions__state",
            )
        )

        descs = {}
        grouped_descriptions = groupby(
            descriptions_dict,
            lambda x: (x["variety__pk"], x["variety__name"], x["name"]),
        )
        for description, description_expressions in grouped_descriptions:
            descs[description] = [e["expressions__state"] for e in list(description_expressions)]
        protocol_traits_states_dict[species]["descriptions"] = descs

        for protocol, traits in protocol_traits_states_dict[species].items():
            if protocol == "descriptions":
                continue

            for trait, states in traits.items():
                expressions = []
                for _, expression_states in descs.items():
                    desc_expressions = []
                    for state_id, state_desc in states["states"].items():
                        if state_id in expression_states:
                            desc_expressions.append(state_desc)
                    expressions.append(desc_expressions)
                protocol_traits_states_dict[species][protocol][trait]["expressions"] = expressions
                non_empty_expressions = [expr for expr in expressions if expr]
                if non_empty_expressions:
                    comparable_expressions = [tuple(sorted(exp)) for exp in non_empty_expressions]
                    protocol_traits_states_dict[species][protocol][trait]["all_equal"] = (
                        len(set(comparable_expressions)) == 1
                    )
                else:
                    protocol_traits_states_dict[species][protocol][trait]["all_equal"] = True
    return descs, protocol_traits_states_dict


def join_description_expressions(
    states_dict: dict[int, str],
    descriptions: dict[tuple, list],
) -> list[list[str]]:
    descriptions_list = []
    for key in descriptions:
        expressions = descriptions[key]
        expression_found = []
        for state_id in states_dict.keys():
            if state_id in expressions:
                expression_found.append(states_dict[state_id])
        descriptions_list.append(expression_found)
    return descriptions_list


def list_elems_equal(expressions: list[list]) -> bool:
    non_empty_items = [expr for expr in expressions if expr]
    if non_empty_items:
        comparable_items = [tuple(sorted(item)) for item in non_empty_items]
        return len(set(comparable_items)) == 1
    return True


def make_traits_expressions_dict(
    traits: QuerySet,
    descriptions_dict: dict[tuple, list],
) -> dict[tuple, dict]:
    res: dict[tuple, dict] = {}
    for trait in traits:
        states = trait.states.all()
        states_dict = {state.pk: f"{state.numeric_id}. {state.description}" for state in states}

        descriptions_expression_str = join_description_expressions(states_dict, descriptions_dict)
        trait_key = (trait.numeric_id, trait.description)
        res[trait_key] = {}
        res[trait_key]["expressions"] = descriptions_expression_str
        res[trait_key]["all_equal"] = list_elems_equal(descriptions_expression_str)

    return res


def make_descriptions_dict(descriptions: QuerySet) -> dict[tuple, dict[tuple, list]]:
    result: dict[tuple, dict[tuple, list]] = {}

    descriptions_dict = descriptions.values(
        "variety__id",
        "variety__name",
        "name",
        species_id=F("protocol__plantspecies__id"),
        species_name=F("protocol__plantspecies__common_name"),
        state_id=F("expressions__state__id"),
    ).order_by(
        "species_id",
        "species_name",
        "variety__id",
        "variety__name",
        "name",
    )

    grouped_species = groupby(
        descriptions_dict,
        lambda x: (x["species_id"], x["species_name"]),
    )

    for species_key, description_data in grouped_species:
        result[species_key] = {}

        grouped_descriptions = groupby(
            description_data,
            lambda x: (
                x["variety__id"],
                x["variety__name"],
                x["name"],
            ),
        )

        for description_key, expressions in grouped_descriptions:
            result[species_key][description_key] = [expression["state_id"] for expression in expressions]

    return result


def make_protocols_dict(
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
