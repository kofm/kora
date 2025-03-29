from itertools import groupby

from django.db.models import QuerySet


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

    descriptions_dict = descriptions.annotated()

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
