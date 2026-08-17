from django.contrib.auth.decorators import permission_required
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.http import HttpResponseBadRequest
from django.shortcuts import get_object_or_404, redirect
from django.template.response import TemplateResponse
from django.urls import reverse
from django.urls.base import reverse_lazy
from django.views.generic.edit import DeleteView
from django_tables2.config import RequestConfig

from breadcrumbs.utils import add_parent_breadcrumbs, generate_breadcrumbs
from calculator.forms import CropUpdateForm
from calculator.models import Crop, CropLayout, ParameterObservation, TraitObservation
from calculator.tables import ParameterObservationTable, TraitObservationTable
from django_sortable_htmx.views import SortableView
from frontpage.headers import DetailHeader


@permission_required("calculator.view_crop", raise_exception=True)
def crop_detail(request, pk):
    partial = request.GET.get("partial", None)
    crop = get_object_or_404(Crop.objects.select_related("variety", "layout__location"), pk=pk)
    is_read_only = crop.layout.is_archived
    context = {"crop": crop, "is_read_only": is_read_only}

    if partial in {None, "trait_observations_table"}:
        trait_observations = TraitObservation.objects.select_related("created_by", "state__trait").filter(crop=crop)
        trait_observations_table = TraitObservationTable(
            trait_observations,
            page_field="obsexpr_page",
            is_read_only=is_read_only,
        )
        RequestConfig(request, paginate={"per_page": 5}).configure(trait_observations_table)
        context["trait_observations_table"] = trait_observations_table

    if partial in {None, "parameter_observations_table"}:
        parameter_observations = ParameterObservation.objects.select_related("created_by", "parameter").filter(
            crop=crop
        )
        parameter_observations_table = ParameterObservationTable(
            parameter_observations,
            page_field="obsparam_page",
            is_read_only=is_read_only,
        )
        RequestConfig(request, paginate={"per_page": 5}).configure(parameter_observations_table)
        context["parameter_observations_table"] = parameter_observations_table

    if partial is None:
        context["header"] = DetailHeader(request, crop, title=crop.variety.name, show_id=True)
        breadcrumbs = generate_breadcrumbs(request, Crop, crop)
        breadcrumbs = add_parent_breadcrumbs(breadcrumbs, crop.layout)
        breadcrumbs = add_parent_breadcrumbs(breadcrumbs, crop.layout.location)
        context.update(breadcrumbs)

    template_name = "calculator/crop_detail.html"
    if partial is not None:
        template_name = f"{template_name}#{partial}"

    return TemplateResponse(request, template_name, context)


@permission_required("calculator.change_crop", raise_exception=True)
def crop_update(request, pk):
    crop = get_object_or_404(
        Crop.objects.mutable().select_related("layout", "variety__species"),
        pk=pk,
    )
    form = CropUpdateForm(request.POST or None, instance=crop)

    if form.is_valid():
        crop = form.save()
        return redirect(reverse("calculator:crop_detail", args=(crop.pk,)))

    breadcrumbs = generate_breadcrumbs(request, Crop, crop)
    context = {"object": crop, "form": form, **breadcrumbs}
    return TemplateResponse(request, "frontpage/_update_form.html", context)


class CropDeleteView(PermissionRequiredMixin, DeleteView):
    model = Crop
    permission_required = "calculator.delete_crop"
    raise_exception = True
    template_name = "frontpage/confirm_delete.html"

    def get_queryset(self):
        return super().get_queryset().mutable()

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        if not self.object.is_deletable:
            return HttpResponseBadRequest("This crop has observations and cannot be deleted.")
        return super().post(request, *args, **kwargs)

    def get_success_url(self):
        return reverse_lazy("calculator:layout_detail", kwargs={"pk": self.object.layout.pk})


class CropSort(PermissionRequiredMixin, SortableView):
    model = Crop
    permission_required = "calculator.change_crop"
    raise_exception = True

    def validate_objects(self, objs):
        layout_ids = {crop.layout_id for crop in objs}
        if len(layout_ids) != 1:
            return HttpResponseBadRequest("Crops must belong to a single layout.")

        layout_id = layout_ids.pop()
        get_object_or_404(CropLayout.objects.visible(), pk=layout_id)
        layout_crop_ids = set(Crop.objects.filter(layout_id=layout_id).values_list("pk", flat=True))
        if {crop.pk for crop in objs} != layout_crop_ids:
            return HttpResponseBadRequest("All crops in the layout must be provided.")
        return None
