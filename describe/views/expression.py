"""Expression Views."""

from django.contrib.auth.decorators import permission_required
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.template.response import TemplateResponse
from django.views.decorators.http import require_GET, require_POST

from describe.forms import ExpressionForm
from describe.models import Description, Expression


@require_GET
def expression_create_form_empty(request, pk, trait):
    """Return a Description ExpressionForm for a specific Trait.

    Used by the `description_update` view via htmx to add an empty field for a specific trait."""
    description = get_object_or_404(Description, pk=pk)
    form = ExpressionForm(initial={"description": description.pk}, trait=trait)
    return TemplateResponse(request, "describe/partials/expression_create.html", {"form": form, "trait": trait})


@require_POST
@permission_required("describe.change_expression", raise_exception=True)
def expression_update_form(request, pk):
    expression = get_object_or_404(Expression, pk=pk)
    form = ExpressionForm(request.POST, instance=expression, trait=expression.state.trait)
    context = {"form": form}
    if form.is_valid():
        form.save()
    return TemplateResponse(request, "describe/partials/expression_update.html", context)


@require_POST
@permission_required("describe.add_expression", raise_exception=True)
def expression_create(request):
    trait = request.POST.get("trait")
    form = ExpressionForm(request.POST, trait=trait)
    if form.is_valid():
        expression = form.save()
        return TemplateResponse(
            request, "describe/partials/expression_update.html", {"form": form, "expression": expression}
        )
    return TemplateResponse(request, "describe/partials/expression_create.html", {"form": form, "trait": trait})


@require_POST
@permission_required("describe.delete_expression", raise_exception=True)
def expression_delete(request, pk):
    expression = get_object_or_404(Expression, pk=pk)
    expression.delete()
    return HttpResponse()
