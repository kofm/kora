import django_tables2 as tables
from django_tables2 import columns
from django.utils.html import format_html
from collect.models import SeedSample
from collect.tables import SeedSampleBaseTable
from describe.models import Description
from describe.tables import DescriptionTable
from parameters.models import ParameterValue

from register.models import Entity, PlantSpecies, PlantVariety, Protection


class CountryRenderer:
    def render_country(self, record):
        return format_html('<i class="{}"></i>', record.country.flag_css)


class ProtectionTable(tables.Table, CountryRenderer):
    type = tables.Column(linkify=True)

    class Meta:
        model = Protection
        template_name = "django_tables2/bootstrap4.html"
        exclude = (
            "id",
            "variety",
        )


class PlantVarietyDescriptionTable(DescriptionTable):
    class Meta:
        model = Description
        exclude = (
            "id",
            "variety",
        )


class PlantVarietyAccessionTable(SeedSampleBaseTable):
    pass


class EntityTable(tables.Table, CountryRenderer):
    name = columns.Column(linkify=True)

    class Meta:
        model = Entity
        fields = ["name", "country", "email"]


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
        fields = [
            "common_name",
            "latin_name",
            "num_varieties",
            "num_accessions",
            "num_parameters",
        ]
        order_by = ["-num_varieties", "common_name"]

    def render_latin_name(self, value, *args):
        return format_html("<i>{}</i>", value)


class PlantVarietyEntityTable(tables.Table):
    name = tables.Column(linkify=True)
    country = tables.TemplateColumn(
        "<i class='{{ record.protection_set.last.country.flag_css }}'></i>",
        verbose_name="Country",
    )

    class Meta:
        model = Entity
        fields = ["name", "species", "country"]


def render_icon(value):
    if value:
        icon = "bi-check"
    else:
        icon = "bi-dash"
    return format_html('<i class="bi {}"></i>', icon)


class PlantVarietyTable(tables.Table):
    name = tables.Column(linkify=True)
    described = tables.Column(empty_values=(), verbose_name="Described", orderable=False)
    accessions = tables.Column(empty_values=(), verbose_name="Accessions", orderable=False)

    class Meta:
        model = PlantVariety
        fields = (
            "name",
            "breeder",
        )

    def render_protected(self, record):
        protected = Protection.objects.filter(variety=record, type="PBR", status="G").exists()
        return render_icon(protected)

    def render_enlisted(self, record):
        enlisted = Protection.objects.filter(variety=record, type__in=["CAT", "NLI"], status="G").exists()
        return render_icon(enlisted)

    def render_described(self, record):
        described = Description.objects.filter(variety=record).exists()
        return render_icon(described)

    def render_accessions(self, record):
        accessions = SeedSample.objects.filter(variety=record).exists()
        return render_icon(accessions)
