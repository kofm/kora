import django_tables2 as tables
from django.forms.widgets import format_html

from collect.models import Sample
from frontpage.tables import TableHoverFixed
from frontpage.utils import smart_truncate_string


class SampleBaseTable(tables.Table):
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
        empty_text = "There are no corresponding seed samples to be displayed."

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
        total = getattr(record, "last_weight", 0) or 0
        available = getattr(record, "available_weight", 0) or 0

        if total == available:
            return total
        return format_html(
            """
                {available} g<del class="text-muted ms-2">{total} g</del>
            """,
            total=total,
            available=available,
        )

    def render_germinability(self, record):
        return str(record.germinability) + "%"


class SampleTable(SampleBaseTable):
    """Extension of the SampleBaseTable for the Accession List.

    It uses HTMX for dynamic content display. See the template for
    details.  It also has (HTMX) action buttons to add Accessions to
    the selected cart.
    """

    variety__name = tables.Column("Variety")
    variety__species__common_name = tables.Column("Species")
    position = tables.Column()
    growing_season = tables.Column("Grown")

    class Meta(SampleBaseTable.Meta):
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


class SampleDuplicatesTable(SampleBaseTable):
    orderable: bool = False

    class Meta(SampleBaseTable.Meta):
        fields = (
            "sample_id",
            "position",
            "weight",
            "growing_season",
            "notes",
            "actions",
        )


class SampleInStorageTable(SampleBaseTable):
    class Meta(SampleBaseTable.Meta):
        fields = (
            "position",
            "sample_id",
            "variety",
            "weight",
            "germinability",
            "growing_season",
            "notes",
            "actions",
        )
