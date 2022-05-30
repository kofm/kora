from typing import Union

from django.db.models.query import QuerySet
from calculator.models import Crop, CropParameter

from parameters.models import SpeciesParameter, VarietalParameter


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
    return (
        Model.objects.filter(**kwargs)
        .values(
            "parameter__code", "value", "parameter__measure_unit", "parameter__name"
        )
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
    return sorted(params_list, key = lambda d: d['parameter__code'])


def get_cropmodels(crop, cropmodels_list):
    # Loop over CROP_MODELS, run the models and store output to the cropmodels list
    import importlib

    cropmodels: list = []
    module = importlib.import_module("calculator.cropmodels")
    for cm in cropmodels_list:
        class_ = getattr(module, cm)
        m = class_(crop)
        if m.can_run():
            cropmodels.append(m.output())
    return {"cropmodels": cropmodels}
