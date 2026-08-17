from calculator.models import Step
from django_sortable_htmx.layouts import BaseSortableGridLayout
from frontpage.layouts import BaseCardLayout, BaseGridLayout


class CropSortableGrid(BaseSortableGridLayout):
    def __init__(self, *args, is_read_only=False, **kwargs):
        super().__init__(*args, **kwargs)
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
        **kwargs,
    ) -> None:
        super().__init__(
            *args,
            num_columns=fieldbook.layout.ncol,
            container_id="fieldbook-grid",
            **kwargs,
        )
        self.add_asset("css", ["calculator/css/fieldbook-grid.css"])
        self.add_asset("js", ["frontpage/selection.js"])
        self.steps = Step.objects.prefetch_related(
            "traittarget", "parametertarget", "traitobservation__state", "parameterobservation"
        ).filter(fieldbook_id=fieldbook.pk)
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
            "planned": False,
            "species_common_name": obj.variety.species.common_name,
        }
        step = self.step_by_crop_map.get(obj.pk)
        if not step:
            return body

        body.update(
            {
                "planned": True,
                "order": step.order + 1,
                "trait_status": self._render_targets(step, "trait"),
                "parameter_status": self._render_targets(step, "parameter"),
                "display_value": self._get_display_value(step),
                "has_display": self.display is not None,
            }
        )
        return body

    def _get_display_value(self, step):
        if self.display is None:
            return ""
        if self.display["model"] == "trait":
            display_value = self._render_trait_observation(step, self.display["id"])
        if self.display["model"] == "parameter":
            field = self.display.get("field", "value")
            display_value = self._render_parameter_observation(step, self.display["id"], field)
        if display_value is None:
            return ""
        return display_value

    def _render_trait_observation(self, step, trait_id):
        observations_by_trait_map = {o.trait_id: o for o in step.traitobservation.all()}
        val = observations_by_trait_map.get(trait_id)
        if val:
            return val.state
        return None

    def _render_parameter_observation(self, step, parameter_id, field="value"):
        observation_by_parameter_map = {o.parameter_id: o for o in step.parameterobservation.all()}
        val = observation_by_parameter_map.get(parameter_id)
        if val:
            return getattr(val, f"parameter_{field}")
        return None

    def _render_targets(self, step, target_type="trait"):
        targets = getattr(step, f"{target_type}target").all()
        target_ids = {getattr(target, f"{target_type}_id") for target in targets}
        if not target_ids:
            return None

        observations = getattr(step, f"{target_type}observation").all()
        observed_ids = {getattr(observation, f"{target_type}_id") for observation in observations}

        if not observed_ids:
            return "pending"
        if observed_ids == target_ids:
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
