from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.db.models import Max
from django.http import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.template.response import TemplateResponse
from django.urls import reverse, reverse_lazy
from django.views.decorators.http import require_POST

from describe.forms import WorkspaceCreateForm, WorkspaceSelectForm, WorkspaceUpdateForm
from describe.models import Description, Workspace, WorkspaceElement
from django_sortable_htmx.views import SortableView


@login_required
@require_POST
def workspace_activate(request):
    workspace_id = request.POST.get("name", None)
    if workspace_id:
        workspace = Workspace.objects.elements().filter(pk=int(workspace_id)).first()
        workspace.is_active = True
        workspace.save()
    else:
        Workspace.objects.all().update(is_active=False)
        workspace = None

    form = WorkspaceSelectForm(request=request)
    return render(
        request,
        "describe/partials/workspaces/workspace_detail.html",
        {"workspace": workspace, "workspace_form": form},
    )


@login_required
def workspace_list(request):
    workspace = Workspace.objects.filter(user=request.user, is_active=True).elements().first()
    form = WorkspaceSelectForm(request=request)
    return render(
        request,
        "describe/partials/workspaces/workspace_detail.html",
        {"workspace": workspace, "workspace_form": form},
    )


@login_required
def workspace_create(request):
    form = WorkspaceCreateForm()
    if request.method == "POST":
        form = WorkspaceCreateForm(request.POST)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.user = request.user
            instance.is_active = True
            instance.save()
            return redirect(reverse("describe:workspace_list"))
    return render(
        request,
        "describe/partials/workspaces/workspace_detail.html",
        {"workspace_form": form},
    )


@login_required
def workspace_update(request, pk):
    instance = get_object_or_404(Workspace, pk=pk)
    if request.method == "POST":
        form = WorkspaceCreateForm(request.POST, instance=instance)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.user = request.user
            instance.save()
            return redirect(reverse("describe:workspace_list"))
    form = WorkspaceUpdateForm(instance=instance)
    return render(
        request,
        "describe/partials/workspaces/workspace_detail.html",
        {"workspace_form": form},
    )


@login_required
def workspace_delete(request, pk):
    desc = get_object_or_404(Workspace, pk=pk)
    if request.POST:
        desc.delete()
        return redirect(reverse_lazy("describe:description_list"))
    return TemplateResponse(request, "frontpage/confirm_delete.html", {"desc": desc})


@login_required
@require_POST
def workspace_element_create(request):
    description_id = request.POST.get("description_id", None)
    workspace = Workspace.objects.filter(user=request.user, is_active=True).elements().first()

    if not description_id or not workspace:
        return JsonResponse({"error": "Invalid input or no active description."}, status=400)

    description = get_object_or_404(Description, pk=description_id)

    with transaction.atomic():
        element, created = WorkspaceElement.objects.get_or_create(description=description, workspace=workspace)
        if not created:
            return JsonResponse({"error": "Element already exists."}, status=400)

        order_max = workspace.descriptions.aggregate(Max("order"))["order__max"]
        if order_max:
            element.order = order_max + 1
            element.save()

    form = WorkspaceSelectForm(request=request)
    return render(
        request,
        "describe/partials/workspaces/workspace_detail.html",
        {"workspace": workspace, "workspace_form": form},
    )


@login_required
def workspace_element_delete(request, pk):
    element = get_object_or_404(WorkspaceElement, pk=pk)
    if request.user == element.workspace.user:
        element.delete()
    return HttpResponse()


class WorkspaceSortableView(SortableView):
    model = WorkspaceElement
