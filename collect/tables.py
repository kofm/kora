import django_tables2 as tables

from collect.models import SampleWeight, SeedSample


class SeedSampleTableMixin:
    def render_germinability(self, record):
        return str(record.germinability) + "%"

    def render_weight(self, record):
        # record.weight == record.weight is just a smart way to check if it's NAN
        # TODO: this should be removed when we can make sure that no
        # NaN values are stored in the db
        return int(record.weight) if record.weight == record.weight else None


class SeedSampleBaseTable(tables.Table, SeedSampleTableMixin):
    sample_id = tables.Column(linkify=True, attrs={"td": {"class": "col-1"}})
    notes = tables.Column(
        attrs={"td": {"class": "text-truncate", "style": "width:10rem; max-width:10rem; min-width:10rem;"}}
    )

    class Meta:
        model = SeedSample
        fields: tuple = (
            "sample_id",
            "growing_season",
            "notes",
        )
        empty_text = "There are no corresponding seed samples to be displayed."


class SeedSampleTable(SeedSampleBaseTable):
    """Extension of the SeedSampleBaseTable for the Accession List.

    It uses HTMX for dynamic content display. See the template for
    details.  It also has (HTMX) action buttons to add Accessions to
    the selected cart.
    """

    variety__name = tables.Column(
        "Variety", attrs={"td": {"class": "col-2"}, "a": {"class": "text-decoration-none link-body-emphasis"}}
    )
    variety__species = tables.Column(
        attrs={
            "td": {"class": "col-2"},
        }
    )
    position = tables.Column(
        attrs={
            "td": {"class": "col-2"},
        }
    )
    growing_season = tables.Column(
        attrs={
            "td": {"class": "col-2"},
        }
    )
    last_weight = tables.Column(
        attrs={
            "td": {"class": "col-2"},
        }
    )
    actions = tables.TemplateColumn(
        template_name="collect/partials/cartitem_add_table_action.html",
        verbose_name="",
        orderable=False,
        attrs={
            "td": {"class": "col-1"},
        },
    )

    class Meta:
        model = SeedSample
        fields = (
            "sample_id",
            "variety__name",
            "variety__species",
            "position",
            "growing_season",
            "last_weight",
            # "last_germinability",
            "notes",
            "actions",
        )
        template_name = "collect/partials/seedsample_table.html"


class SeedSampleDuplicatesTable(SeedSampleBaseTable):
    orderable = False

    class Meta(SeedSampleBaseTable.Meta):
        fields = (
            "sample_id",
            "variety",
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


class SampleWeightTable(tables.Table):
    class Meta:
        model = SampleWeight
        fields = ("created_at", "weight")
