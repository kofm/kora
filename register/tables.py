import django_tables2 as tables
from django.utils.html import format_html

from calculator.models import Crop
from collect.models import Sample
from collect.tables import BaseSampleTable
from describe.models import Description
from frontpage.tables import EditDeleteColumn, TableHoverFixed
from frontpage.utils.text import smart_truncate_string
from parameters.models import VarietalParameter
from register.models import Entity, PlantSpecies, PlantVariety, PlantVarietyName, Protection


class CountryRenderer:
    def render_country(self, record):
        return format_html('<i class="{}"></i>', record.country.flag_css)


class PlantVarietyCropTable(tables.Table):
    id = tables.Column(verbose_name="Crop", linkify=True)
    layout = tables.Column(linkify=True, attrs={"a": {"class": "row-link"}})
    location = tables.Column(accessor="layout.location", linkify=True, attrs={"a": {"class": "row-link"}})

    class Meta(TableHoverFixed.Meta):
        model = Crop
        fields = ("id", "layout", "location", "notes")
        per_page = 10
        empty_text = "There are no crops in visible layouts."


class PlantVarietyNameTable(tables.Table):
    actions = EditDeleteColumn()

    class Meta(TableHoverFixed.Meta):
        model = PlantVarietyName
        fields = ("name", "change_date", "actions")
        per_page = 5


class ProtectionTable(tables.Table, CountryRenderer):
    actions = EditDeleteColumn()
    type = tables.Column(attrs={"td": {"class": "fw-bold"}})
    date_start = tables.Column(attrs={"td": {"class": "text-muted"}})
    date_end = tables.Column(attrs={"td": {"class": "text-muted"}})
    note = tables.Column(attrs={"td": {"class": "fw-light"}})

    class Meta(TableHoverFixed.Meta):
        model = Protection
        exclude = ("id", "variety")
        per_page = 5


class ProtectionListTable(ProtectionTable):
    variety = tables.Column(attrs={"td": {"class": "fw-bold"}})
    status = tables.Column(attrs={"td": {"class": "fw-light"}})
    type = tables.Column()

    class Meta(TableHoverFixed.Meta):
        model = Protection
        fields = (
            "variety",
            "type",
            "status",
            "country",
            "note",
        )
        exclude = ("date_start", "date_end", "reference", "actions")
        template_name = "register/partials/protection_table.html"
        per_page = 10
        empty_text = "There are no protections to be displayed."

    def render_note(self, record):
        notes = smart_truncate_string(record.note, 18)
        return f"{notes}"


class PlantVarietyDescriptionTable(tables.Table):
    protocol__name = tables.Column("Protocol", attrs={"td": {"class": "fw-bold"}})
    updated_at = tables.DateTimeColumn(verbose_name="Last updated", short=False)
    notes = tables.Column("Notes")
    actions = tables.TemplateColumn(
        template_name="register/partials/description_table_actions.html",
        verbose_name="",
        orderable=False,
    )

    class Meta(TableHoverFixed.Meta):
        model = Description
        fields = ("protocol__name", "label")
        per_page = 5

    def render_label(self, record, value):
        return format_html(
            '<span class="badge rounded-pill {} text-nowrap"><small>{}</small></span>',
            value.colour_class,
            value,
        )

    def render_notes(self, record):
        notes = smart_truncate_string(record.notes, min_length=25)
        return f"{notes}"


class PlantVarietySampleTable(BaseSampleTable):
    actions = tables.TemplateColumn(
        template_name="collect/partials/sample_table_actions.html",
        verbose_name="",
        orderable=False,
    )

    class Meta(BaseSampleTable.Meta):
        model = Sample
        fields = (
            "sample_id",
            "position",
            "weight",
            "growing_season",
            "notes",
            "actions",
        )
        per_page = 5


class EntityTable(tables.Table, CountryRenderer):
    name = tables.Column(attrs={"td": {"class": "fw-bold"}})
    type = tables.Column(attrs={"td": {"class": "text-muted"}})

    class Meta(TableHoverFixed.Meta):
        model = Entity
        fields = ("name", "type", "country")
        template_name = "register/partials/entity_table.html"
        per_page = 10
        empty_text = "There are no matching entities."


class VarietalParameterTable(tables.Table):
    value = tables.Column(orderable=False)
    parameter__name = tables.Column("Parameter", attrs={"td": {"class": "fw-bold"}})
    parameter__code = tables.Column("Code", attrs={"td": {"class": "fw-light"}})
    note = tables.Column("Notes", attrs={"td": {"class": "fw-light"}})

    actions = EditDeleteColumn()

    class Meta:
        attrs = {"class": "table table-hover table-fixed small-table compact-table"}
        model = VarietalParameter
        template_name = "django_tables2/bootstrap5.html"
        fields = ("parameter__name", "parameter__code", "value", "note")
        per_page = 5

    def render_value(self, record):
        return record.get_value_display()


class PlantSpeciesTable(tables.Table):
    id = tables.Column("#")
    common_name = tables.Column(attrs={"td": {"class": "fw-bold"}})
    botanical_name = tables.Column(verbose_name="Botanical name", attrs={"td": {"class": "fst-italic"}})
    code = tables.Column(attrs={"td": {"class": "fw-light"}})
    actions = EditDeleteColumn()

    class Meta(TableHoverFixed.Meta):
        model = PlantSpecies
        fields = ("id", "common_name", "botanical_name", "code")
        order_by = "common_name"
        template_name = "frontpage/partials/htmx_table.html"
        empty_text = "There are no matching plant species."

    def render_id(self, value):
        return format_html('<span class="detail-page-id-badge">{}</span>', value)


class PlantVarietyEntityTable(tables.Table):
    name = tables.Column(linkify=True)

    class Meta:
        model = PlantVariety
        fields = ("name", "species")


def render_icon(value):
    icon = "bi-check" if value else "bi-dash"
    return format_html('<i class="bi {}"></i>', icon)
