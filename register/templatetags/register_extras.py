from django import template

from parameters.models import CropParameter

register = template.Library()


@register.filter
def get_last_parameters_value(cropparameter_set):
    return cropparameter_set.order_by("parameter", "-updated_at").distinct("parameter")
