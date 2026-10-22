from typing import Any

import django_tables2 as tables
from django.utils.html import format_html

from collect.models import Sample
from frontpage.tables import TableHoverFixed
from frontpage.utils.text import smart_truncate_string


class BaseSampleTable(tables.Table):
    weight = tables.Column(
        verbose_name="Stock",
        orderable=False,
        attrs={"td": {"class": "text-nowrap"}},
    )
    growing_season = tables.Column("Grown", attrs={"td": {"class": "text-muted"}})
    notes = tables.Column(attrs={"td": {"class": "text-nowrap text-truncate fw-light"}})
    actions = tables.TemplateColumn(
        template_name="collect/partials/sample_table_actions.html",
        verbose_name="",
        orderable=False,
    )

    class Meta(TableHoverFixed.Meta):
        attrs = {"class": "table table-hover table-fixed small-table compact-table"}
        model = Sample
        fields: tuple = ("sample_id", "growing_season", "notes")
        empty_text = "There are no matching samples."
        row_attrs: dict[str, Any] = TableHoverFixed.Meta.row_attrs | {
            "class": lambda record: "table-danger" if record.is_being_discarded else ""
        }

    def render_sample_id(self, value):
        return format_html('<span class="detail-page-id-badge">{}</span>', value)

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
    """Extension of the SampleBaseTable for the Sample List.

    It uses HTMX for dynamic content display. See the template for
    details.  It also has (HTMX) action buttons to add Samples to
    the selected cart.
    """

    variety__name = tables.Column("Variety", attrs={"td": {"class": "fw-bold"}})
    variety__species__common_name = tables.Column("Species", attrs={"td": {"class": "fw-light"}})
    position = tables.Column()

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
    """Extension of the SampleBaseTable for the Sample List.

    It uses HTMX for dynamic content display. See the template for
    details.  It also has (HTMX) action buttons to add Samples to
    the selected cart.
    """

    variety__name = tables.Column("Variety", attrs={"td": {"class": "fw-bold"}})
    variety__species__common_name = tables.Column("Species", attrs={"td": {"class": "fw-light"}})
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
    position__name = tables.Column("Position")
    variety = tables.Column(attrs={"td": {"class": "fw-bold"}})

    class Meta(BaseSampleTable.Meta):
        fields = (
            "position__name",
            "sample_id",
            "variety",
            "weight",
            "growing_season",
            "notes",
            "actions",
        )
        per_page = 20
