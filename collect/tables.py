from django.utils.html import format_html
import django_tables2 as tables

from collect.models import SeedSample


class SeedSampleTableMixin:
    def render_germinability(self, record):
        return str(record.germinability) + "%"

    def render_weight(self, record):
        # record.weight == record.weight is just a smart way to check if it's NAN
        # TODO: this should be removed when we can make sure that no
        # NaN values are stored in the db
        return int(record.weight) if record.weight == record.weight else None

    def render_variety(self, record):
        if record.variety.breeder:
            return format_html(
                "{} <i class='{}'></i>",
                record.variety.name,
                record.variety.breeder.country.flag_css,
            )
        else:
            return record.variety


class SeedSampleBaseTable(tables.Table, SeedSampleTableMixin):
    sample_id = tables.Column(linkify=True, attrs={"td": {"class": "col-1"}})
    germinability = tables.Column(verbose_name="Germinability")
    weight = tables.Column(verbose_name="Weight (g)")
    notes = tables.Column(attrs={"td": {"class": "col-3"}})

    class Meta:
        model = SeedSample
        fields = (
            "sample_id",
            "position",
            "weight",
            "germinability",
            "growing_season",
            "notes",
        )
        empty_text = "There are no corresponding seed samples to be displayed."


class SeedSampleTable(SeedSampleBaseTable):
    """
    An extension of the SeedSampleBaseTable for the Accession List. It
    uses HTMX for dynamic content display. See the template for details.
    It also has (HTMX) action buttons to add Accessions to the
    selected cart.
    """
    variety = tables.Column(
        attrs={
            "td": {"class": "col-2"},
            "a": {"class": "text-decoration-none link-body-emphasis"},
        }
    )
    actions = tables.TemplateColumn(
        template_name="collect/partials/cartitem_add_table_action.html",
        verbose_name="",
        orderable=False,
    )

    class Meta:
        fields = (
            "sample_id",
            "variety",
            "position",
            "weight",
            "germinability",
            "growing_season",
            "notes",
            "actions",
        )
        template_name = "collect/partials/seedsample_table.html"


class SeedSampleDuplicatesTable(SeedSampleBaseTable):
    orderable = False

    class Meta(SeedSampleBaseTable.Meta):
        fields = (
            "sample_id",
            "position",
            "weight",
            "germinability",
            "growing_season",
            "notes",
        )


class SeedSampleInStorageTable(SeedSampleBaseTable):

    class Meta(SeedSampleBaseTable.Meta):
        fields = (
            "sample_id",
            "position",
            "variety",
            "weight",
            "germinability",
            "growing_season",
            "notes",
        )
