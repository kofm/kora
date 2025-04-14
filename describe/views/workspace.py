from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.db.models import Max
from django.http import HttpResponse, HttpResponseBadRequest, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.views.decorators.http import require_POST

from describe.forms import WorkspaceCreateForm, WorkspaceSelectForm, WorkspaceUpdateForm
from describe.models import Description, Workspace, WorkspaceElement
from django_sortable_htmx.views import SortableView


@login_required
@require_POST
def workspace_activate(request):
    form = WorkspaceSelectForm(request.POST, user=request.user)
    if form.is_valid() and "workspace" in request.POST:
        form.save()
        return redirect(reverse("describe:workspace_detail"))
    return HttpResponseBadRequest()


@login_required
def workspace_detail(request):
    workspace = Workspace.objects.elements().filter(user=request.user, is_active=True).first()
    form = WorkspaceSelectForm(user=request.user, initial={"workspace": workspace})
    return render(
        request,
        "describe/partials/workspace_detail.html",
        {"workspace": workspace, "workspace_form": form},
    )


@login_required
def workspace_create(request):
    form = WorkspaceCreateForm()
    if request.method == "POST":
        form = WorkspaceCreateForm(request.POST)
        if form.is_valid():
            workspace = form.save(commit=False)
            workspace.user = request.user
            workspace.is_active = True
            workspace.save()
            return redirect(reverse("describe:workspace_detail"))
    return render(
        request,
        "describe/partials/workspace_detail.html",
        {"workspace_form": form},
    )


@login_required
def workspace_update(request, pk):
    workspace = get_object_or_404(Workspace, pk=pk)
    if request.method == "POST":
        form = WorkspaceCreateForm(request.POST, instance=workspace)
        if form.is_valid():
            workspace = form.save(commit=False)
            workspace.user = request.user
            workspace.save()
            return redirect(reverse("describe:workspace_detail"))
    form = WorkspaceUpdateForm(instance=workspace)
    return render(
        request,
        "describe/partials/workspace_detail.html",
        {"workspace_form": form},
    )


@login_required
def workspace_delete(request, pk):
    workspace = get_object_or_404(Workspace, pk=pk)
    if request.method == "POST":
        workspace.delete()
        return redirect(reverse("describe:workspace_detail"))
    return render(request, "describe/partials/workspace_confirm_delete.html", {"workspace": workspace})


@login_required
@require_POST
def workspace_element_create(request):
    description_id = request.POST.get("description_id", None)
    workspace = Workspace.objects.filter(user=request.user, is_active=True).first()

    if not description_id or not workspace:
        return JsonResponse({"error": "Invalid input or no active description."}, status=409)

    description = get_object_or_404(Description, pk=description_id)

    with transaction.atomic():
        element, created = WorkspaceElement.objects.get_or_create(description=description, workspace=workspace)
        if not created:
            return JsonResponse({"error": "Element already exists."}, status=400)

        order_max = workspace.descriptions.aggregate(Max("order"))["order__max"]
        if order_max:
            element.order = order_max + 1
            element.save()

    return redirect(reverse("describe:workspace_detail"))


@login_required
def workspace_element_delete(request, pk):
    element = get_object_or_404(WorkspaceElement, pk=pk)
    if request.user == element.workspace.user:
        element.delete()
    return HttpResponse()


class WorkspaceSortableView(SortableView):
    model = WorkspaceElement
