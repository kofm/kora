from typing import Union

from django.db.models.query import QuerySet
from calculator.models import Crop, CropParameter

from parameters.models import SpeciesParameter, VarietalParameter

import pandas as pd


def get_available_params(queryset: QuerySet) -> set:
    available_params = set([x["parameter__code"] for x in queryset])
    return available_params


def get_params(queryset: QuerySet, params_list: list) -> list:
    queryset = queryset.filter(parameter__code__in=params_list).distinct(
        "parameter__code"
    )
    return list(queryset)


def get_all_params(
    Model: Union[CropParameter, VarietalParameter, SpeciesParameter], **kwargs
) -> QuerySet:
    return Model.objects.filter(**kwargs).values(
        "parameter",
        "parameter__code",
        "value",
        "parameter__measure_unit",
        "parameter__name",
    )


def get_crop_params_list(crop: Crop) -> list:
    """
    Returns a list of parameters retrieved prioritized in the following order:
    Crop -> PlantVariety -> PlantSpecies
    meaning that returns a list of dictionaries which is the most comprehensive
    set of parameters from the three classes
    """
    cropparams = get_all_params(CropParameter, crop=crop)
    found_cropparams = get_available_params(cropparams)
    found_varparams = set()
    found_speciesparams = set()
    params_list = list(cropparams)
    if crop.has_variety():
        varparams = get_all_params(VarietalParameter, variety=crop.variety)
        found_varparams = get_available_params(varparams) - found_cropparams
        params_list += get_params(varparams, found_varparams)
    if crop.has_species():
        speciesparams = get_all_params(SpeciesParameter, specie=crop.species)
        found_speciesparams = (
            get_available_params(speciesparams) - found_cropparams - found_varparams
        )
        params_list += get_params(speciesparams, found_speciesparams)
    return sorted(params_list, key=lambda d: d["parameter__code"])


def get_cropmodels(crop, cropmodels):
    import importlib

    cropmodels_outputs = []
    for module_name, cropmodel_class in cropmodels:
        module = importlib.import_module(f"cropmodels.{module_name}")
        class_ = getattr(module, cropmodel_class)
        model = class_(crop)
        if model.can_run():
            cropmodels_outputs.append(model.output())
    return {"cropmodels": cropmodels_outputs}


def format_unit(model_name: str, measure_unit: str):
    if measure_unit != "":
        return f"{model_name} ({measure_unit})"
    else:
        return f"{model_name}"


def crop_statistics_calc(crop_queryset: QuerySet, models):
    crop_statistics = pd.DataFrame()
    if crop_queryset:
        cropmodels_results = [get_cropmodels(crop, models) for crop in crop_queryset]
        crompodels_results_dict = [
            {
                format_unit(
                    cropmodels_result["model_name"], cropmodels_result["measure_unit"]
                ): cropmodels_result["value"]
                for cropmodels_result in cropmodels_result_row["cropmodels"]
            }
            for cropmodels_result_row in cropmodels_results
        ]
        crop_statistics = (
            pd.DataFrame(
                [
                    {
                        **{
                            "common_name": crop.species.common_name,
                            "total_area": crop.area.total_area,
                            **cropmodels_result,
                        }
                    }
                    for crop, cropmodels_result in zip(
                        crop_queryset, crompodels_results_dict
                    )
                ]
            )
            .groupby("common_name")
            .sum()
            .reset_index()
        )
    return crop_statistics
