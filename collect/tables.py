import django_tables2 as tables

from collect.models import Sample, SampleWeight
from frontpage.utils import smart_truncate_string


class SampleTableMixin:
    def render_germinability(self, record):
        return str(record.germinability) + "%"


class SampleTablePositionMixin:
    def render_position(self, record):
        return f"{record.position.storage.name}-{record.position.name}"


class SampleBaseTable(tables.Table, SampleTableMixin):
    sample_id = tables.Column(linkify=True, attrs={"td": {"class": "col-1"}})
    notes = tables.Column(
        attrs={
            "td": {
                "class": "text-truncate",
                "style": "width:10rem; max-width:10rem; min-width:10rem;",
            }
        }
    )

    class Meta:
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


class SampleTable(SampleTablePositionMixin, SampleBaseTable):
    """Extension of the SampleBaseTable for the Accession List.

    It uses HTMX for dynamic content display. See the template for
    details.  It also has (HTMX) action buttons to add Accessions to
    the selected cart.
    """

    variety__name = tables.Column(
        "Variety",
        attrs={
            "td": {"class": "col-2"},
            "a": {"class": "text-decoration-none link-body-emphasis"},
        },
    )
    variety__species__common_name = tables.Column(attrs={"td": {"class": "col-2"}})
    position = tables.Column(attrs={"td": {"class": "col-2"}})
    growing_season = tables.Column(
        attrs={
            "td": {"class": "col-2"},
        }
    )
    last_weight = tables.Column(
        "Weight (g)",
        attrs={
            "td": {"class": "col-2"},
        },
    )
    actions = tables.TemplateColumn(
        template_name="collect/partials/sample_table_actions.html",
        verbose_name="",
        orderable=False,
        attrs={
            "td": {"class": "col-1"},
        },
    )

    class Meta:
        model = Sample
        fields = (
            "sample_id",
            "variety__name",
            "variety__species__common_name",
            "position",
            "growing_season",
            "last_weight",
            "notes",
            "actions",
        )
        template_name = "collect/partials/sample_table.html"


class SampleDuplicatesTable(SampleTablePositionMixin, SampleBaseTable):
    orderable: bool = False

    class Meta(SampleBaseTable.Meta):
        fields = (
            "sample_id",
            "position",
            "last_weight",
            "last_germinability",
            "growing_season",
            "notes",
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
        )


class SampleWeightTable(tables.Table):
    class Meta:
        model = SampleWeight
        fields = ("created_at", "weight")
