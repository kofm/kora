from dataclasses import dataclass

from django.core.exceptions import ValidationError
from django.db import transaction
from django.db.models import Count, F, Max, Q

from calculator.models import FieldBook, ParameterObservation, ParameterTarget, Step, TraitObservation, TraitTarget


@dataclass(frozen=True)
class TargetPlan:
    fieldbook: FieldBook
    crop: object
    related_object: object
    required_count: int = 1
    row_index: int = 0


class TargetPlanValidationError(Exception):
    def __init__(self, errors):
        self.errors = errors
        super().__init__("Invalid target plans")


def target_field_name(target_model):
    if target_model is TraitTarget:
        return "trait"
    if target_model is ParameterTarget:
        return "parameter"
    raise TypeError(f"Unsupported target model: {target_model!r}")


def target_identity(plan):
    return (plan.fieldbook.pk, plan.crop.pk, plan.related_object.pk)


def validate_target_plan(target_model, plan):
    field_name = target_field_name(target_model)
    errors = {}
    if plan.fieldbook.layout_id != plan.crop.layout_id:
        errors["crop"] = "The crop must belong to the field book layout."
    if plan.required_count < 1:
        errors["required_count"] = "Ensure this value is greater than or equal to 1."
    if plan.required_count > 32767:
        errors["required_count"] = "Ensure this value is less than or equal to 32767."
    if plan.fieldbook.layout.is_archived:
        errors["fieldbook"] = "Targets cannot be changed in an archived layout."
    if target_model is TraitTarget and plan.crop.variety.species_id != plan.related_object.protocol.plantspecies_id:
        errors[field_name] = "The trait species must match the crop variety species."
    return errors


def find_target(target_model, plan):
    field_name = target_field_name(target_model)
    return target_model.objects.filter(
        step__fieldbook=plan.fieldbook,
        step__crop=plan.crop,
        **{field_name: plan.related_object},
    ).first()


def validate_target_identity(target_model, plan):
    errors = validate_target_plan(target_model, plan)
    if errors:
        raise ValidationError(errors)
    existing = find_target(target_model, plan)
    if existing is None:
        return None
    if existing.required_count == plan.required_count:
        return existing
    raise ValidationError(
        {"required_count": "This target already exists with a different required count; delete and recreate it."}
    )


def duplicate_errors(plans):
    indexes_by_identity = {}
    for plan in plans:
        indexes_by_identity.setdefault(target_identity(plan), []).append(plan.row_index)

    errors = {}
    for indexes in indexes_by_identity.values():
        if len(indexes) > 1:
            message = "Duplicate target identity in this request."
            errors.update({index: {"non_field_errors": message} for index in indexes})
    return errors


@transaction.atomic
def create_targets(target_model, plans):
    if not plans:
        return [], 0

    errors = duplicate_errors(plans)
    field_name = target_field_name(target_model)
    fieldbook_ids = sorted({plan.fieldbook.pk for plan in plans})
    locked_fieldbooks = {
        fieldbook.pk: fieldbook
        for fieldbook in FieldBook.objects.select_for_update().select_related("layout").filter(pk__in=fieldbook_ids)
    }
    normalized_plans = [
        TargetPlan(
            fieldbook=locked_fieldbooks[plan.fieldbook.pk],
            crop=plan.crop,
            related_object=plan.related_object,
            required_count=plan.required_count,
            row_index=plan.row_index,
        )
        for plan in plans
    ]

    crop_ids = {plan.crop.pk for plan in normalized_plans}
    related_object_ids = {plan.related_object.pk for plan in normalized_plans}
    steps = list(
        Step.objects.filter(fieldbook_id__in=fieldbook_ids)
        .filter(crop_id__in=crop_ids)
        .select_related("fieldbook", "crop")
    )
    steps_by_placement = {(step.fieldbook_id, step.crop_id): step for step in steps}

    target_relations = ["step__fieldbook", "step__crop", field_name]
    if target_model is TraitTarget:
        target_relations.append("trait__protocol")
    existing_targets = target_model.objects.filter(
        step__fieldbook_id__in=fieldbook_ids,
        step__crop_id__in=crop_ids,
        **{f"{field_name}_id__in": related_object_ids},
    ).select_related(*target_relations)
    existing_targets_by_identity = {
        (target.step.fieldbook_id, target.step.crop_id, getattr(target, f"{field_name}_id")): target
        for target in existing_targets
    }

    for plan in normalized_plans:
        row_errors = validate_target_plan(target_model, plan)
        existing = existing_targets_by_identity.get(target_identity(plan))
        if existing is not None and existing.required_count != plan.required_count:
            row_errors["required_count"] = (
                "This target already exists with a different required count; delete and recreate it."
            )
        if row_errors:
            errors[plan.row_index] = {**errors.get(plan.row_index, {}), **row_errors}

    if errors:
        row_errors = [{} for _ in plans]
        for index, error in errors.items():
            row_errors[index] = error
        raise TargetPlanValidationError(row_errors)

    next_orders = {
        row["fieldbook_id"]: row["maximum_order"] + 1
        for row in Step.objects.filter(fieldbook_id__in=fieldbook_ids)
        .values("fieldbook_id")
        .annotate(maximum_order=Max("order"))
    }
    for fieldbook_id in fieldbook_ids:
        next_orders.setdefault(fieldbook_id, 0)

    missing_steps = []
    for plan in normalized_plans:
        placement = (plan.fieldbook.pk, plan.crop.pk)
        if placement not in steps_by_placement:
            step = Step(
                fieldbook=plan.fieldbook,
                crop=plan.crop,
                order=next_orders[plan.fieldbook.pk],
            )
            next_orders[plan.fieldbook.pk] += 1
            steps_by_placement[placement] = step
            missing_steps.append(step)
    Step.objects.bulk_create(missing_steps)

    missing_targets = []
    for plan in normalized_plans:
        if target_identity(plan) not in existing_targets_by_identity:
            target = target_model(
                step=steps_by_placement[(plan.fieldbook.pk, plan.crop.pk)],
                required_count=plan.required_count,
                **{field_name: plan.related_object},
            )
            existing_targets_by_identity[target_identity(plan)] = target
            missing_targets.append(target)
    target_model.objects.bulk_create(missing_targets)

    results = [existing_targets_by_identity[target_identity(plan)] for plan in normalized_plans]
    return results, len(missing_targets)


def target_observations(target):
    if isinstance(target, TraitTarget):
        return TraitObservation.objects.filter(step_id=target.step_id, state__trait_id=target.trait_id)
    if isinstance(target, ParameterTarget):
        return ParameterObservation.objects.filter(step_id=target.step_id, parameter_id=target.parameter_id)
    raise TypeError(f"Unsupported target: {target!r}")


def trait_observation_counts_by_trait(step):
    observation_counts = (
        TraitObservation.objects.filter(step=step).values("state__trait_id").annotate(recorded_count=Count("pk"))
    )
    return {row["state__trait_id"]: row["recorded_count"] for row in observation_counts}


def parameter_observation_counts_by_parameter(step):
    observation_counts = (
        ParameterObservation.objects.filter(step=step).values("parameter_id").annotate(recorded_count=Count("pk"))
    )
    return {row["parameter_id"]: row["recorded_count"] for row in observation_counts}


def target_recorded_count(target):
    return target_observations(target).count()


def target_is_complete(target):
    return target_recorded_count(target) >= target.required_count


def observation_target(observation):
    if isinstance(observation, TraitObservation) and observation.step_id:
        return TraitTarget.objects.filter(step_id=observation.step_id, trait_id=observation.state.trait_id).first()
    if isinstance(observation, ParameterObservation) and observation.step_id:
        return ParameterTarget.objects.filter(
            step_id=observation.step_id,
            parameter_id=observation.parameter_id,
        ).first()
    return None


def target_has_observation(target):
    return target_observations(target).exists()


@transaction.atomic
def change_required_count(target, delta):
    target = target.__class__.objects.select_for_update().select_related("step__fieldbook__layout").get(pk=target.pk)
    if target.step.fieldbook.layout.is_archived:
        raise ValidationError("Targets cannot be changed in an archived layout.")
    recorded_count = target_recorded_count(target)
    minimum_count = max(1, recorded_count)
    new_count = target.required_count + delta
    if new_count < minimum_count:
        raise ValidationError(f"Required count cannot be less than {minimum_count}.")
    target.required_count = new_count
    target.full_clean()
    target.save(update_fields=["required_count"])
    return target


def observed_target_query(target_model):
    if target_model is TraitTarget:
        return Q(step__traitobservation__state__trait_id=F("trait_id"))
    if target_model is ParameterTarget:
        return Q(step__parameterobservation__parameter_id=F("parameter_id"))
    raise TypeError(f"Unsupported target model: {target_model!r}")


def clear_stale_display_config(fieldbook):
    display_config = fieldbook.display_config
    if not display_config:
        return
    target_model = TraitTarget if display_config["model"] == "trait" else ParameterTarget
    field_name = display_config["model"]
    if not target_model.objects.filter(
        step__fieldbook=fieldbook,
        **{f"{field_name}_id": display_config["id"]},
    ).exists():
        fieldbook.display_config = None
        fieldbook.save(update_fields=["display_config"])


@transaction.atomic
def delete_target(target):
    if target.step.fieldbook.layout.is_archived:
        raise ValidationError("Targets cannot be changed in an archived layout.")
    if target_has_observation(target):
        raise ValidationError("The target cannot be removed because it has already been observed.")
    fieldbook = target.step.fieldbook
    target.delete()
    clear_stale_display_config(fieldbook)
