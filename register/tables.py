import django_tables2 as tables
from django.utils.html import format_html
from django_tables2 import columns

from collect.models import Sample
from collect.tables import SampleBaseTable
from describe.models import Description
from frontpage.tables import TableHoverFixed
from frontpage.utils.text import smart_truncate_string
from parameters.models import ParameterValue
from register.models import Entity, PlantSpecies, PlantVariety, Protection


class CountryRenderer:
    def render_country(self, record):
        return format_html('<i class="{}"></i>', record.country.flag_css)


class ProtectionTable(tables.Table, CountryRenderer):
    type = tables.Column(linkify=True)

    class Meta:
        model = Protection
        exclude = ("id", "variety")
        per_page = 5


class ProtectionListTable(ProtectionTable):
    variety = tables.Column(linkify=True)

    class Meta:
        model = Protection
        fields = (
            "variety",
            "type",
            "status",
            "country",
            "reference",
            "date_start",
            "date_end",
            "note",
        )
        template_name = "register/partials/protection_table.html"
        per_page = 10

    def render_note(self, record):
        notes = smart_truncate_string(record.note, 18)
        return f"{notes}"


class PlantVarietyDescriptionTable(tables.Table):
    name = tables.Column(linkify=True)
    protocol__name = tables.Column("Protocol")
    actions = tables.TemplateColumn(
        template_name="register/partials/description_table_actions.html",
        verbose_name="",
        orderable=False,
    )

    class Meta(TableHoverFixed.Meta):
        model = Description
        fields = ("name", "protocol__name")
        per_page = 5


class PlantVarietySampleTable(SampleBaseTable):
    actions = tables.TemplateColumn(
        template_name="collect/partials/sample_table_actions.html",
        verbose_name="",
        orderable=False,
    )

    class Meta(SampleBaseTable.Meta):
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
    name = columns.Column(linkify=True)

    class Meta:
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
    num_varieties = tables.Column(verbose_name="Varieties")
    num_accessions = tables.Column(verbose_name="Accessions")
    num_parameters = tables.Column(verbose_name="Parameters")

    class Meta:
        model = PlantSpecies
        fields = ("common_name", "latin_name", "num_varieties", "num_accessions", "num_parameters")
        order_by = ("-num_varieties", "common_name")

    def render_latin_name(self, value):
        return format_html("<i>{}</i>", value)


class PlantVarietyEntityTable(tables.Table):
    name = tables.Column(linkify=True)
    country = tables.TemplateColumn(
        "<i class='{{ record.protection_set.last.country.flag_css }}'></i>",
        verbose_name="Country",
    )

    class Meta:
        model = Entity
        fields = ("name", "species", "country")


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

    def render_protected(self, record):
        protected = Protection.objects.filter(variety=record, type="PBR", status="G").exists()
        return render_icon(protected)

    def render_enlisted(self, record):
        enlisted = Protection.objects.filter(variety=record, type__in=("CAT", "NLI"), status="G").exists()
        return render_icon(enlisted)

    def render_described(self, record):
        described = Description.objects.filter(variety=record).exists()
        return render_icon(described)

    def render_accessions(self, record):
        accessions = Sample.objects.filter(variety=record).exists()
        return render_icon(accessions)
