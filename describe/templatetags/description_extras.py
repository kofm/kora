from django import template

from describe.models import Description

register = template.Library()


@register.filter
def filter_expression_by_trait(expression, trait_id):
    return expression.filter(state__trait_id=trait_id)


@register.filter
def descriptions_with_this_protocol(protocol_id):
    return Description.objects.filter(protocol_id=protocol_id)
