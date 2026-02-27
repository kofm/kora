import django_tables2 as tables

from collect.models import Sample
from frontpage.tables import TableHoverFixed
from frontpage.utils.text import smart_truncate_string


class BaseSampleTable(tables.Table):
    weight = tables.Column(
        verbose_name="Stock",
        orderable=False,
        attrs={"td": {"class": "text-nowrap"}},
    )
    growing_season = tables.Column("Grown")
    notes = tables.Column(attrs={"td": {"class": "text-nowrap text-truncate"}})
    actions = tables.TemplateColumn(
        template_name="collect/partials/sample_table_actions.html",
        verbose_name="",
        orderable=False,
    )

    class Meta(TableHoverFixed.Meta):
        model = Sample
        fields: tuple = (
            "sample_id",
            "growing_season",
            "notes",
        )
        empty_text = "There are no matching seed samples to be displayed."
        row_attrs = TableHoverFixed.Meta.row_attrs | {
            "class": lambda record: "table-danger" if record.is_being_discarded else ""
        }

    def render_notes(self, record):
        notes = smart_truncate_string(record.notes)
        return f"{notes}"

    def render_position(self, record):
        return f"{record.position.storage.name}-{record.position.name}"

    def render_weight(self, record, value):
        """
        record.last_weight  → total grams
        record.available_weight → available grams
        """
        return record.get_weight_display()

    def render_germinability(self, record):
        return str(record.germinability) + "%"


class SampleTable(BaseSampleTable):
    """Extension of the SampleBaseTable for the Accession List.

    It uses HTMX for dynamic content display. See the template for
    details.  It also has (HTMX) action buttons to add Accessions to
    the selected cart.
    """

    variety__name = tables.Column("Variety")
    variety__species__common_name = tables.Column("Species")
    position = tables.Column()
    growing_season = tables.Column("Grown")

    class Meta(BaseSampleTable.Meta):
        model = Sample
        fields = (
            "sample_id",
            "variety__name",
            "variety__species__common_name",
            "position",
            "growing_season",
            "weight",
            "notes",
            "actions",
        )
        template_name = "collect/partials/sample_table.html"


class DiscardedSampleTable(BaseSampleTable):
    """Extension of the SampleBaseTable for the Accession List.

    It uses HTMX for dynamic content display. See the template for
    details.  It also has (HTMX) action buttons to add Accessions to
    the selected cart.
    """

    variety__name = tables.Column("Variety")
    variety__species__common_name = tables.Column("Species")
    growing_season = tables.Column("Grown")
    actions = tables.TemplateColumn(
        template_name="collect/partials/discarded_sample_table_actions.html",
        verbose_name="",
        orderable=False,
    )

    class Meta(BaseSampleTable.Meta):
        model = Sample
        fields = (
            "sample_id",
            "variety__name",
            "variety__species__common_name",
            "growing_season",
            "weight",
            "notes",
            "actions",
        )
        template_name = "collect/partials/discarded_sample_table.html"
        row_attrs = {}


class DuplicatedSampleTable(BaseSampleTable):
    orderable: bool = False

    class Meta(BaseSampleTable.Meta):
        fields = (
            "sample_id",
            "position",
            "weight",
            "growing_season",
            "notes",
            "actions",
        )


class SampleInStorageTable(BaseSampleTable):
    class Meta(BaseSampleTable.Meta):
        fields = (
            "sample_id",
            "variety",
            "weight",
            "growing_season",
            "notes",
            "actions",
        )
        per_page = 15
