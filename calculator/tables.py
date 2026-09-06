import django_tables2 as tables
from django.contrib.humanize.templatetags.humanize import naturalday
from django.urls import reverse

from calculator.models import (
    CropLayout,
    CropParameter,
    FieldBook,
    ManagementType,
    ParameterObservation,
    TraitObservation,
)
from frontpage.tables import TableHoverFixed


class ManagementTypeTable(tables.Table):
    actions = tables.TemplateColumn(
        template_name="calculator/partials/managementtype_table_actions.html",
        verbose_name="",
        orderable=False,
        attrs={"td": {"class": "text-end"}},
    )

    class Meta(TableHoverFixed.Meta):
        model = ManagementType
        fields = ("code", "name", "description", "actions")
        template_name = "frontpage/partials/htmx_table.html"
        empty_text = "There are no management types."
        per_page = 15


class BaseCropLayoutTable(tables.Table):
    name = tables.Column(linkify=True)
    crop_count = tables.Column(verbose_name="Crops", orderable=False)
    fieldbook_count = tables.Column(verbose_name="Field books", orderable=False)

    class Meta(TableHoverFixed.Meta):
        model = CropLayout
        fields: tuple = ("name", "crop_count", "fieldbook_count")
        template_name = "frontpage/partials/htmx_table.html"
        per_page = 10


class CropLayoutTable(BaseCropLayoutTable):
    class Meta(BaseCropLayoutTable.Meta):
        fields = (*BaseCropLayoutTable.Meta.fields, "updated_at")
        empty_text = "There are no active layouts."


class CropLayoutListTable(BaseCropLayoutTable):
    location = tables.Column()
    status = tables.Column(orderable=False, empty_values=())

    class Meta(BaseCropLayoutTable.Meta):
        fields = ("name", "location", "status", "crop_count", "fieldbook_count", "updated_at")
        empty_text = "There are no crop layouts."

    def render_status(self, record):
        return "Archived" if record.archived_at else "Visible"


class BaseFieldBookTable(tables.Table):
    name = tables.Column(linkify=True)
    observation_count = tables.Column(verbose_name="Observations", orderable=False)
    planned_target_count = tables.Column(verbose_name="Planned", orderable=False)
    percent_completed = tables.Column(verbose_name="Completion", orderable=False)

    class Meta(TableHoverFixed.Meta):
        model = FieldBook
        fields: tuple = ("name", "observation_count", "planned_target_count", "percent_completed")
        template_name = "frontpage/partials/htmx_table.html"
        empty_text = "There are no fieldbooks."
        per_page = 10

    def render_percent_completed(self, record, value):
        return f"{value:.1f}%"


class FieldBookTable(BaseFieldBookTable):
    layout = tables.Column()
    location = tables.Column(accessor="layout.location")

    class Meta(BaseFieldBookTable.Meta):
        model = FieldBook
        fields = ("name", "layout", "location")
        per_page = 15


class FieldBookInLayoutTable(BaseFieldBookTable):
    pass


class CropParameterTable(tables.Table):
    class Meta:
        model = CropParameter
        fields = ["parameter__code", "value"]


class ObservationMutationTable(tables.Table):
    mutation_view_name = ""

    def __init__(self, *args, is_read_only=False, **kwargs):
        super().__init__(*args, **kwargs)
        if not is_read_only:
            self.row_attrs.update(
                {
                    "hx-target": "#modal",
                    "hx-get": lambda record: reverse(self.mutation_view_name, args=(record.pk,)),
                    "hx-swap": "innerHTML",
                    "hx-trigger": "click",
                    "data-bs-toggle": "modal",
                    "data-bs-target": "#modal",
                    "role": "button",
                }
            )


class TraitObservationTable(ObservationMutationTable):
    mutation_view_name = "calculator:trait_observation_update"

    class Meta:
        model = TraitObservation
        fields = ("state__trait", "state", "state__trait__protocol", "notes", "recorded_at", "created_by")
        template_name = "frontpage/partials/htmx_table.html"
        empty_text = "Nothing here."
        attrs = {"class": "table table-hover table-fixed small-table"}


class TraitObservationListTable(tables.Table):
    variety = tables.Column(accessor="crop.variety")
    layout = tables.Column(accessor="crop.layout", linkify=True)
    fieldbook = tables.Column(accessor="step.fieldbook", linkify=True)
    protocol = tables.Column(accessor="state.trait.protocol", orderable=False)
    trait = tables.Column(accessor="state.trait", orderable=False)
    state = tables.Column(orderable=False)
    recorded_at = tables.Column(verbose_name="Date")

    class Meta:
        model = TraitObservation
        fields = ("variety", "layout", "fieldbook", "protocol", "trait", "state", "recorded_at")
        template_name = "frontpage/partials/htmx_table.html"
        empty_text = "There are no trait observations."
        attrs = {"class": "table table-hover table-fixed small-table"}
        row_attrs = {
            "_": lambda record: f"on click go to url '{record.crop.get_absolute_url()}#expressions'",
            "role": "button",
        }

    def render_recorded_at(self, value):
        return naturalday(value)


class ParameterObservationTable(ObservationMutationTable):
    mutation_view_name = "calculator:parameter_observation_update"

    class Meta:
        model = ParameterObservation
        fields = ("parameter", "parameter_value", "parameter_date", "notes", "recorded_at", "created_by")
        template_name = "frontpage/partials/htmx_table.html"
        attrs = {"class": "table table-hover table-fixed small-table"}
        empty_text = "Nothing here."


class ParameterObservationListTable(tables.Table):
    variety = tables.Column(accessor="crop.variety")
    layout = tables.Column(accessor="crop.layout", linkify=True)
    fieldbook = tables.Column(accessor="step.fieldbook", linkify=True)
    parameter = tables.Column(orderable=False)
    recorded_at = tables.Column(verbose_name="Recorded date")
    created_by = tables.Column(verbose_name="Recorder", orderable=False)

    class Meta:
        model = ParameterObservation
        fields = (
            "variety",
            "layout",
            "fieldbook",
            "parameter",
            "parameter_value",
            "parameter_date",
            "notes",
            "recorded_at",
            "created_by",
        )
        template_name = "frontpage/partials/htmx_table.html"
        empty_text = "There are no parameter observations."
        attrs = {"class": "table table-hover table-fixed small-table"}
        row_attrs = {
            "_": lambda record: f"on click go to url '{record.crop.get_absolute_url()}#obs_parameters'",
            "role": "button",
        }

    def render_recorded_at(self, value):
        return naturalday(value)
