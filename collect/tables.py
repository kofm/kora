from django.utils.html import format_html
import django_tables2 as tables

from collect.models import SeedSample


class SeedSampleTableMixin:
    def render_germinability(self, record):
        return str(record.germinability) + "%"

    def render_weight(self, record):
        # record.weight == record.weight is just a smart way to check if it's NAN
        # TODO: it shouldn't be possible to store nan in db
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


class SeedSampleTable(tables.Table, SeedSampleTableMixin):
    sample_id = tables.Column(linkify=True)
    variety = tables.Column()
    germinability = tables.Column(verbose_name="Germinability")
    weight = tables.Column(verbose_name="Weight (g)")
    actions = tables.TemplateColumn(
        """
        <a class="text-decoration-none link-dark" hx-post="{% url "collect:cartitem-add" record.pk %}" hx-target="#cart" hx-include="#default-weight" href="#" data-bs-toggle="offcanvas" data-bs-target="#cart" aria-controls="cart"><i class="bi bi-bag-plus-fill"></i></a>
        """,
        verbose_name="",
        orderable=False,
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.columns["sample_id"].column.attrs = {"td": {"class": "col-1"}}
        self.columns["variety"].column.attrs = {
            "td": {"class": "col-2"},
            "a": {"class": "text-decoration-none link-dark"},
        }
        self.columns["notes"].column.attrs = {"td": {"class": "col-3"}}

    class Meta:
        model = SeedSample
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
        empty_text = "There are no corresponding seed samples to be displayed."


class SeedSampleDuplicatesTable(tables.Table, SeedSampleTableMixin):
    orderable = False

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
        empty_text = "There are no seed samples to be displayed."
