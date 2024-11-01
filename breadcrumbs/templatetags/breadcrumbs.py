from django import template
from ..utils import CONTEXT_KEY

register = template.Library()


@register.inclusion_tag("breadcrumbs/crumbs.html", takes_context=True)
def render_breadcrumbs(context):
    return {"crumbs": context[CONTEXT_KEY]}
