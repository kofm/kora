import django_tables2 as tables
from django.contrib.humanize.templatetags.humanize import naturalday
from django.urls import reverse

from calculator.models import CropLayout, CropParameter, ParameterObservation, TraitObservation
from frontpage.tables import TableHoverFixed


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
        fields = ("state__trait", "state", "notes", "recorded_at", "created_by")
        template_name = "frontpage/partials/htmx_table.html"
        empty_text = "Nothing here."
        attrs = {"class": "table table-hover table-fixed small-table"}


class TraitObservationListTable(tables.Table):
    variety = tables.Column(accessor="crop.variety", orderable=False)
    layout = tables.Column(accessor="crop.layout")
    protocol = tables.Column(accessor="state.trait.protocol", orderable=False)
    trait = tables.Column(accessor="state.trait", orderable=False)
    state = tables.Column(orderable=False)
    recorded_at = tables.Column(verbose_name="Date")

    class Meta:
        model = TraitObservation
        fields = ("variety", "layout", "protocol", "trait", "state", "recorded_at")
        template_name = "frontpage/partials/htmx_table.html"
        empty_text = "There are no trait observations."
        attrs = {"class": "table table-hover table-fixed"}
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
    variety = tables.Column(accessor="crop.variety", orderable=False)
    layout = tables.Column(accessor="crop.layout")
    parameter = tables.Column(orderable=False)
    recorded_at = tables.Column(verbose_name="Recorded date")
    created_by = tables.Column(verbose_name="Recorder", orderable=False)

    class Meta:
        model = ParameterObservation
        fields = (
            "variety",
            "layout",
            "parameter",
            "parameter_value",
            "parameter_date",
            "notes",
            "recorded_at",
            "created_by",
        )
        template_name = "frontpage/partials/htmx_table.html"
        empty_text = "There are no parameter observations."
        attrs = {"class": "table table-hover table-fixed"}
        row_attrs = {
            "_": lambda record: f"on click go to url '{record.crop.get_absolute_url()}#obs_parameters'",
            "role": "button",
        }

    def render_recorded_at(self, value):
        return naturalday(value)
