from django.contrib import messages
from django.contrib.auth.decorators import permission_required
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.db import transaction
from django.db.models import Max
from django.http import HttpResponse, HttpResponseBadRequest, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.views.decorators.http import require_POST

from describe.forms import WorkspaceCreateForm, WorkspaceSelectForm, WorkspaceUpdateForm
from describe.models import Description, Workspace, WorkspaceElement
from django_sortable_htmx.views import SortableView


@permission_required("describe.view_workspace", raise_exception=True)
@require_POST
def workspace_activate(request):
    form = WorkspaceSelectForm(request.POST, user=request.user)
    if form.is_valid() and "workspace" in request.POST:
        form.save()
        return redirect(reverse("describe:workspace_detail"))
    return HttpResponseBadRequest()


@permission_required("describe.view_workspace", raise_exception=True)
def workspace_detail(request):
    workspace = Workspace.objects.elements().filter(user=request.user, is_active=True).first()
    form = WorkspaceSelectForm(user=request.user, initial={"workspace": workspace})
    return render(
        request,
        "describe/partials/workspace_detail.html",
        {"workspace": workspace, "workspace_form": form},
    )


@permission_required("describe.add_workspace", raise_exception=True)
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


@permission_required("describe.change_workspace", raise_exception=True)
def workspace_update(request, pk):
    workspace = get_object_or_404(Workspace, pk=pk, user=request.user)
    if request.method == "POST":
        form = WorkspaceCreateForm(request.POST, instance=workspace)
        if form.is_valid():
            workspace = form.save()
            return redirect(reverse("describe:workspace_detail"))
    form = WorkspaceUpdateForm(instance=workspace)
    return render(
        request,
        "describe/partials/workspace_detail.html",
        {"workspace_form": form},
    )


@permission_required("describe.delete_workspace", raise_exception=True)
def workspace_delete(request, pk):
    workspace = get_object_or_404(Workspace, pk=pk, user=request.user)
    if request.method == "POST":
        workspace.delete()
        return redirect(reverse("describe:workspace_detail"))
    return render(request, "describe/partials/workspace_confirm_delete.html", {"workspace": workspace})


@permission_required("describe.add_workspaceelement", raise_exception=True)
@require_POST
def workspace_element_create(request):
    description_id = request.POST.get("description_id", None)
    if not description_id:
        return JsonResponse({"error": "Invalid input"}, status=409)

    workspace = Workspace.objects.filter(user=request.user, is_active=True).first()
    if not workspace:
        messages.error(request, "No workspace selected.")
        return HttpResponse(headers={"HX-Reswap": "none"})

    description = get_object_or_404(Description, pk=description_id)

    with transaction.atomic():
        element, created = WorkspaceElement.objects.get_or_create(description=description, workspace=workspace)
        if not created:
            messages.warning(request, f"{description} is already in Workspace '{workspace.name}'")
            return HttpResponse(headers={"HX-Reswap": "none"})

        order_max = workspace.descriptions.aggregate(Max("order"))["order__max"]
        element.order = order_max + 1 if order_max else 1
        element.save()
        messages.success(request, f"{description} added to Workspace '{workspace.name}'")

    return redirect(reverse("describe:workspace_detail"))


@permission_required("describe.delete_workspaceelement", raise_exception=True)
@require_POST
def workspace_element_delete(request, pk):
    element = get_object_or_404(WorkspaceElement, pk=pk, workspace__user=request.user)
    element.delete()
    return HttpResponse()


class WorkspaceSortableView(PermissionRequiredMixin, SortableView):
    model = WorkspaceElement
    permission_required = ["describe.change_workspaceelement"]
    raise_exception = True

    def get_queryset(self):
        return WorkspaceElement.objects.filter(workspace__user=self.request.user, workspace__is_active=True)
