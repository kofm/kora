import django_tables2 as tables
from django.utils.html import format_html

from collect.models import Sample
from collect.tables import BaseSampleTable
from describe.models import Description
from frontpage.tables import TableHoverFixed
from frontpage.utils.text import smart_truncate_string
from parameters.models import ParameterValue
from register.models import Entity, PlantSpecies, PlantVariety, Protection


class CountryRenderer:
    def render_country(self, record):
        return format_html('<i class="{}"></i>', record.country.flag_css)


class ProtectionTable(tables.Table, CountryRenderer):
    class Meta(TableHoverFixed.Meta):
        model = Protection
        exclude = ("id", "variety")
        per_page = 5


class ProtectionListTable(ProtectionTable):
    variety = tables.Column(linkify=True)

    class Meta(TableHoverFixed.Meta):
        model = Protection
        fields = (
            "variety",
            "type",
            "status",
            "country",
            "note",
        )
        exclude = ("date_start", "date_end", "reference")
        template_name = "register/partials/protection_table.html"
        per_page = 10

    def render_note(self, record):
        notes = smart_truncate_string(record.note, 18)
        return f"{notes}"


class PlantVarietyDescriptionTable(tables.Table):
    protocol__name = tables.Column("Protocol")
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
            "growing_season",
            "weight",
            "notes",
            "actions",
        )
        per_page = 5


class EntityTable(tables.Table, CountryRenderer):
    class Meta(TableHoverFixed.Meta):
        model = Entity
        fields = ("name", "type", "country")
        template_name = "register/partials/entity_table.html"
        per_page = 10


class VarietalParameterTable(tables.Table):
    """Table display of varietal parameters."""

    actions = tables.TemplateColumn(
        template_name="parameters/partials/varietalparameter_table_actions.html",
        verbose_name="",
        orderable=False,
        attrs={"td": {"class": "text-end"}},
    )

    class Meta:
        model = ParameterValue
        page_field = "para_page"
        template_name = "django_tables2/bootstrap4.html"
        fields = ("parameter__name", "parameter__code", "value", "url_ref", "note")
        per_page = 5

    def render_value(self, record):
        return format_html("{} {}", record.value, record.parameter.measure_unit)


class PlantSpeciesTable(tables.Table):
    common_name = tables.Column(linkify=True)
    latin_name = tables.Column(verbose_name="Latin name")

    class Meta:
        model = PlantSpecies
        fields = ("common_name", "latin_name")
        order_by = "common_name"

    def render_latin_name(self, value):
        return format_html("<i>{}</i>", value)


class PlantVarietyEntityTable(tables.Table):
    name = tables.Column(linkify=True)

    class Meta:
        model = PlantVariety
        fields = ("name", "species")


def render_icon(value):
    icon = "bi-check" if value else "bi-dash"
    return format_html('<i class="bi {}"></i>', icon)


class PlantVarietyTable(tables.Table):
    name = tables.Column(linkify=True)
    described = tables.Column(empty_values=(), verbose_name="Described", orderable=False)
    accessions = tables.Column(empty_values=(), verbose_name="Accessions", orderable=False)

    class Meta:
        model = PlantVariety
        fields = ("name", "breeder")
        empty_text = "No cultivars have been catalogued under this plant species."

    def render_described(self, record):
        described = Description.objects.filter(variety=record).exists()
        return render_icon(described)

    def render_accessions(self, record):
        accessions = Sample.objects.filter(variety=record).exists()
        return render_icon(accessions)
