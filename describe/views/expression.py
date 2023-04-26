"""
Expression Views
"""


from django.views.generic import UpdateView

from describe.models import Expression


class ExpressionUpdate(UpdateView):
    model = Expression
    fields = "__all__"
    template_name = "describe/expression_update.html"
