"""DescriptionsList Views."""

from django.db import transaction
from django.contrib.auth.decorators import login_required
from django.db.models import Max
from django.http import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.template.response import TemplateResponse
from django.urls import reverse_lazy
from django.views.decorators.http import require_POST

from describe.forms import DescriptionsUserListCreateForm
from describe.models import Description, DescriptionsUserList, DescriptionsUserListElement


@login_required
def descriptionsuserlist_create(request):
    form = DescriptionsUserListCreateForm()
    if request.method == "POST":
        form = DescriptionsUserListCreateForm(request.POST)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.user = request.user
            instance.save()
            return redirect(reverse_lazy("describe:description-list"))
    return TemplateResponse(
        request, "describe/descriptionsuserlist_form.html", {"form": form, "object_to_create": "List"}
    )


@login_required
def descriptionsuserlist_delete(request, pk):
    desc = get_object_or_404(DescriptionsUserList, pk=pk)
    if request.POST:
        desc.delete()
        return redirect(reverse_lazy("describe:description-list"))
    return TemplateResponse(request, "frontpage/confirm_delete.html", {"desc": desc})


@login_required
@require_POST
def descriptionsuserlistelement_create(request):
    description_id = request.POST.get("description_id", None)
    active_list = request.user.descriptionsuserlist_set.filter(is_active=True).first()

    if not description_id or not active_list:
        return JsonResponse({"error": "Invalid input or no active description."}, status=400)

    description = get_object_or_404(Description, pk=description_id)

    with transaction.atomic():
        element, created = DescriptionsUserListElement.objects.get_or_create(
            description=description, desc_list=active_list
        )
        if not created:
            return JsonResponse({"error": "Element already exists."}, status=400)

        order_max = active_list.descriptions.aggregate(Max("order"))["order__max"]
        if order_max:
            element.order = order_max + 1
            element.save()

    return render(
        request,
        "describe/partials/descriptionsuserlist_detail_list_item.html",
        {"object": element},
    )


@login_required
def descriptionsuserlistelement_delete(request, pk):
    elem = get_object_or_404(DescriptionsUserListElement, pk=pk)
    if request.user == elem.desc_list.user:
        elem.delete()
    return HttpResponse()


@login_required
@require_POST
def descriptionsuserlist_activate(request):
    descriptionsuserlist_id = request.POST.get("name", None)
    if descriptionsuserlist_id:
        descriptionsuserlist = get_object_or_404(DescriptionsUserList, pk=int(descriptionsuserlist_id))
        descriptionsuserlist.is_active = True
        descriptionsuserlist.save()
    else:
        DescriptionsUserList.objects.all().update(is_active=False)
        descriptionsuserlist = None
    return render(
        request,
        "describe/partials/descriptionsuserlist_detail_ul.html",
        {"descriptionsuserlist": descriptionsuserlist},
    )
