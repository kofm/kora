from django.urls import reverse

from calculator.models import Step
from django_sortable_htmx.layouts import BaseSortableGridLayout
from frontpage.layouts import BaseCardLayout, BaseGridLayout


class CropSortableGrid(BaseSortableGridLayout):
    template_name = "calculator/partials/crop_sortable_grid.html"

    def __init__(self, *args, is_read_only=False, **kwargs):
        super().__init__(*args, show_coordinates=True, **kwargs)
        if is_read_only:
            self.template_name = "frontpage/partials/grid.html"

    def get_title(self, obj):
        return obj.variety.name

    def get_body(self, obj):
        return obj.variety.species.common_name


class FieldBookGrid(BaseGridLayout):
    item_template_name = "calculator/step/partials/grid_item.html"

    def __init__(
        self,
        *args,
        fieldbook,
        highlighted: str | None = None,
        display: dict | None = None,
        can_add_trait_observation=False,
        can_add_parameter_observation=False,
        can_change_trait_observation=False,
        can_change_parameter_observation=False,
        **kwargs,
    ) -> None:
        super().__init__(
            *args,
            num_columns=fieldbook.layout.ncol,
            container_id="fieldbook-grid",
            show_coordinates=True,
            **kwargs,
        )
        self.add_asset("css", ["calculator/css/fieldbook-grid.css"])
        self.add_asset("js", ["frontpage/selection.js"])
        self.steps = Step.objects.prefetch_related(
            "traittarget", "parametertarget", "traitobservation__state", "parameterobservation"
        ).filter(fieldbook_id=fieldbook.pk)
        self.is_read_only = fieldbook.layout.is_archived
        self.can_add_trait_observation = can_add_trait_observation
        self.can_add_parameter_observation = can_add_parameter_observation
        self.can_change_trait_observation = can_change_trait_observation
        self.can_change_parameter_observation = can_change_parameter_observation
        self.step_by_crop_map = {s.crop_id: s for s in self.steps}
        self.highlighted = highlighted
        self.display = self._validate_display(display or fieldbook.display_config)

    def _validate_display(self, display):
        if display is None:
            return None

        if not isinstance(display, dict):
            raise ValueError("`display` must be a dictionary.")

        if "model" not in display or "id" not in display:
            raise ValueError("`display` must contain at least 'model' and 'id' keys")

        model = display["model"]
        if model not in {"trait", "parameter"}:
            raise ValueError("`display.model` must be either 'trait' or 'parameter'")

        if not isinstance(display["id"], int):
            raise ValueError("`display.id` must be an integer")

        if "field" in display and display["field"] not in {"value", "date"}:
            raise ValueError("`field` value must be either 'value' or 'date'")

        return display

    def get_title(self, obj):
        return obj.variety.name

    def get_body(self, obj):
        body = {
            "in_walk": False,
            "planned": False,
            "species_common_name": obj.variety.species.common_name,
        }
        step = self.step_by_crop_map.get(obj.pk)
        if not step:
            return body

        trait_status = self._render_targets(step, "trait")
        parameter_status = self._render_targets(step, "parameter")
        body.update(
            {
                "in_walk": True,
                "planned": trait_status is not None or parameter_status is not None,
                "order": step.order + 1,
                "trait_status": trait_status,
                "parameter_status": parameter_status,
                **self._get_display_data(step),
                "has_display": self.display is not None,
            }
        )
        return body

    def _get_display_data(self, step):
        data = {"display_value": None, "display_mutation_url": "", "display_mutation_label": ""}
        if self.display is None:
            return data

        model = self.display["model"]
        target_id = self.display["id"]
        targets = getattr(step, f"{model}target").all()
        target = next((target for target in targets if getattr(target, f"{model}_id") == target_id), None)
        if target is None:
            return data

        observations = getattr(step, f"{model}observation").all()
        matching_observations = [
            observation for observation in observations if getattr(observation, f"{model}_id") == target_id
        ]
        observation = max(
            matching_observations,
            key=lambda observation: (observation.recorded_at, observation.pk),
            default=None,
        )
        if observation is not None:
            if model == "trait":
                data["display_value"] = observation.state
                can_change = self.can_change_trait_observation
                update_view_name = "calculator:trait_observation_update"
            else:
                field = self.display.get("field", "value")
                data["display_value"] = getattr(observation, f"parameter_{field}")
                can_change = self.can_change_parameter_observation
                update_view_name = "calculator:parameter_observation_update"

        is_complete = len(matching_observations) >= target.required_count
        can_add = self.can_add_trait_observation if model == "trait" else self.can_add_parameter_observation
        if not is_complete and can_add and not self.is_read_only:
            data["display_mutation_url"] = reverse(
                f"calculator:{model}_target_observation_create",
                args=(target.pk,),
            )
            data["display_mutation_label"] = "Record observation"
        elif observation is not None and can_change and not self.is_read_only:
            data["display_mutation_url"] = reverse(update_view_name, args=(observation.pk,))
            data["display_mutation_label"] = "Update observation"
        return data

    def _render_targets(self, step, target_type="trait"):
        targets = getattr(step, f"{target_type}target").all()
        if not targets:
            return None

        observations = getattr(step, f"{target_type}observation").all()
        observed_counts = {}
        for observation in observations:
            object_id = getattr(observation, f"{target_type}_id")
            observed_counts[object_id] = observed_counts.get(object_id, 0) + 1

        fulfilled_count = 0
        required_count = 0
        for target in targets:
            object_id = getattr(target, f"{target_type}_id")
            required_count += target.required_count
            fulfilled_count += min(target.required_count, observed_counts.get(object_id, 0))

        if fulfilled_count == 0:
            return "pending"
        if fulfilled_count == required_count:
            return "complete"
        return "partial"

    def get_item_css_class(self, obj):
        if str(obj.pk) == self.highlighted:
            return "bg-info"
        return ""

    def get_url(self, obj):
        step = self.step_by_crop_map.get(obj.pk)
        if step:
            return step.get_absolute_url()
        return ""


class FieldBookCardLayout(BaseCardLayout):
    def get_title(self, obj):
        return f"{obj.name}"
