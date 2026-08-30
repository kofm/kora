from collections import defaultdict

from django.contrib import messages
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.core.exceptions import BadRequest, ImproperlyConfigured, ValidationError
from django.db import transaction
from django.db.models import Max
from django.forms import BaseForm
from django.http import HttpResponseBadRequest
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse
from django.views import View

from calculator.models import FieldBook, Step, Target
from calculator.targets import delete_target
from frontpage.utils.htmx import htmx_response_trigger
from frontpage.views_decorators import is_htmx


class BaseTargetCreate(PermissionRequiredMixin, View):
    model: type[Target] | None = None
    form_class: type[BaseForm] | None = None
    field_name: str | None = None
    permission_required = "calculator.change_fieldbook"
    raise_exception = True

    def get_selected_crops(self, request, fieldbook):
        selection = request.POST.getlist("selection")
        if not selection:
            raise BadRequest()

        selected_crop_ids = set(selection)
        selected_crops = list(
            fieldbook.layout.crops.select_related("variety__species").filter(pk__in=selected_crop_ids)
        )

        if len(selected_crops) != len(selected_crop_ids):
            raise BadRequest()

        return selected_crops

    def get_compatible_crops_and_count(self, selected_crops, target_obj):
        skipped_crop_count = 0
        return selected_crops, skipped_crop_count

    def post(self, request, fieldbook_id):
        if self.model is None or not issubclass(self.model, Target):
            raise ImproperlyConfigured(f"{self.__class__.__name__} requires a Target `model`")
        if self.form_class is None or not issubclass(self.form_class, BaseForm):
            raise ImproperlyConfigured(
                f"{self.__class__.__name__} requires a form_class that is a subclass of django.forms.Form."
            )
        if self.field_name is None:
            raise ImproperlyConfigured("`field_name` not defined.")

        fieldbook = get_object_or_404(
            FieldBook.objects.mutable().select_related("layout").prefetch_related("steps__crop__variety"),
            pk=fieldbook_id,
        )
        selected_crops = self.get_selected_crops(request, fieldbook)

        form = self.form_class(request.POST)

        if not form.is_valid():
            return HttpResponseBadRequest()

        target_obj = form.cleaned_data[self.field_name]
        compatible_crops, skipped_crop_count = self.get_compatible_crops_and_count(selected_crops, target_obj)

        steps_qs = fieldbook.steps.all()
        steps_by_crop_map = {step.crop_id: step for step in steps_qs}
        order_max = steps_qs.aggregate(max=Max("order", default=-1))["max"] + 1
        targets = self.model.objects.filter(step__in=steps_qs.values_list("pk", flat=True))
        target_by_step_map = defaultdict(list)
        for target in targets:
            target_obj_id = getattr(target, f"{self.field_name}_id")
            target_by_step_map[target.step_id].append(target_obj_id)

        targets_to_create, steps_to_create = [], []
        for crop in compatible_crops:
            crop_id = crop.pk
            step = steps_by_crop_map.get(crop_id)
            if not step:
                step = Step(fieldbook_id=fieldbook_id, crop_id=crop_id, order=order_max)
                order_max += 1
                steps_to_create.append(step)
            step_targets_ids = target_by_step_map.get(step.pk, ())
            if target_obj.pk not in step_targets_ids:
                target = self.model(step=step, **{self.field_name: target_obj})
                targets_to_create.append(target)

        with transaction.atomic():
            if steps_to_create:
                Step.objects.bulk_create(steps_to_create)
            if targets_to_create:
                self.model.objects.bulk_create(targets_to_create)

        target_count = len(targets_to_create)
        if target_count:
            messages.success(
                request,
                f"One {self.field_name} to be observed across {target_count} "
                f"crop{'s' if target_count > 1 else ''} added to the fieldbook.",
            )
        if skipped_crop_count:
            messages.warning(
                request,
                f"The {self.field_name} was skipped for {skipped_crop_count} incompatible "
                f"crop{'s' if skipped_crop_count > 1 else ''}.",
            )
        return redirect(reverse("calculator:fieldbook_detail", args=(fieldbook_id,)))


class BaseTargetDelete(PermissionRequiredMixin, View):
    model: type[Target] | None = None
    permission_required = "calculator.change_fieldbook"
    raise_exception = True

    def post(self, request, pk):
        if self.model is None or not issubclass(self.model, Target):
            raise ImproperlyConfigured(f"{self.__class__.__name__} requires a Target `model`")

        target = get_object_or_404(
            self.model.objects.mutable().select_related("step__fieldbook__layout"),
            pk=pk,
        )

        step_id = target.step_id
        try:
            delete_target(target)
        except ValidationError as exc:
            return HttpResponseBadRequest(exc.messages[0])

        if is_htmx(request):
            event_name = (
                "traitObservationUpdated"
                if self.model._meta.model_name == "traittarget"
                else "observationParameterUpdated"
            )
            return htmx_response_trigger([event_name])
        return redirect("calculator:step_detail", pk=step_id)
