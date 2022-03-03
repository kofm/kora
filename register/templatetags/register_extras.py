from django import template

from parameters.models import SpeciesParameter

register = template.Library()

@register.filter
def get_last_parameters_value(speciesparameter_set):
    return speciesparameter_set.order_by("parameter", "-updated_at").distinct("parameter")
