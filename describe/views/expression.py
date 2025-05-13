"""Expression Views."""

from django.contrib.auth.decorators import permission_required
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.template.response import TemplateResponse
from django.views.decorators.http import require_POST

from describe.forms import ExpressionForm
from describe.models import Expression, State


@require_POST
@permission_required("describe.change_expression", raise_exception=True)
def expression_update(request, pk):
    expression = get_object_or_404(Expression.objects.select_related("state"), pk=pk)
    state_queryset = State.objects.filter(trait=expression.state.trait_id)
    form = ExpressionForm(request.POST, instance=expression)
    form.fields["state"].queryset = state_queryset
    if form.is_valid():
        form.save()
    return TemplateResponse(request, "describe/partials/expression_update.html", {"form": form})


@permission_required("describe.add_expression", raise_exception=True)
def expression_create(request):
    if request.method == "POST":
        form = ExpressionForm(request.POST)
        trait = request.POST.get("trait")
        state_choices = State.objects.filter(trait=trait)
        form.fields["state"].queryset = state_choices
        if form.is_valid():
            expression = form.save()
            return TemplateResponse(
                request, "describe/partials/expression_update.html", {"form": form, "expression": expression}
            )
    else:
        description = request.GET.get("description", None)
        form = ExpressionForm(initial={"description": description})
        trait = request.GET.get("trait")
        state_choices = State.objects.filter(trait=trait)
        form.fields["state"].queryset = state_choices
    return TemplateResponse(request, "describe/partials/expression_create.html", {"form": form, "trait": trait})


@require_POST
@permission_required("describe.delete_expression", raise_exception=True)
def expression_delete(request, pk):
    expression = get_object_or_404(Expression, pk=pk)
    expression.delete()
    return HttpResponse()
