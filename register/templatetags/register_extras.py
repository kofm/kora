from django import template

register = template.Library()

@register.filter
def get_last_parameters_value(parameters):
    return parameters.order_by("parameter", "-updated_at").distinct("parameter")
