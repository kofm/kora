from django.utils.html import format_html
import django_tables2 as tables

from collect.models import SeedSample


class SeedSampleTable(tables.Table):
    sample_id = tables.Column(linkify=True)
    variety = tables.Column()
    germinability = tables.Column(verbose_name="Germinability")
    weight = tables.Column(verbose_name="Weight (g)")
    actions = tables.TemplateColumn(
        """
        <a class="text-decoration-none link-dark" href="{% url "register:plantvariety-detail" record.variety.pk %}"><i class="bi bi-flower1"></i></a>
        <a class="text-decoration-none link-dark" href="{% url "collect:cartitem-add" record.pk %}"><i class="bi bi-list"></i></a>
        """,
        verbose_name="",
        orderable=False
    )


    def __init__(
        self,
        data=None,
        order_by=None,
        orderable=None,
        empty_text=None,
        exclude=None,
        attrs=None,
        row_attrs=None,
        pinned_row_attrs=None,
        sequence=None,
        prefix=None,
        order_by_field=None,
        page_field=None,
        per_page_field=None,
        template_name=None,
        default=None,
        request=None,
        show_header=None,
        show_footer=True,
        extra_columns=None
    ):
        super().__init__(
            data,
            order_by,
            orderable,
            empty_text,
            exclude,
            attrs,
            row_attrs,
            pinned_row_attrs,
            sequence,
            prefix,
            order_by_field,
            page_field,
            per_page_field,
            template_name,
            default,
            request,
            show_header,
            show_footer,
            extra_columns
        )
        self.columns['sample_id'].column.attrs = {"td":{"class" : "col-1" }}
        self.columns['variety'].column.attrs = {"td":{"class" : "col-2" }, "a": {"class": "text-decoration-none link-dark"}}
        self.columns['notes'].column.attrs = {"td":{"class" : "col-3" }}

    def render_germinability(self, record):
        return str(record.germinability) + "%"

    def render_weight(self, record):
        # record.weight == record.weight is just a smart way to check if it's NAN
        # TODO: it shouldn't be possible to store nan in db
        return int(record.weight) if record.weight == record.weight else None

    def render_variety(self, record):
        if record.variety.breeder:
            return format_html("{} <i class='{}'></i>", record.variety.name, record.variety.breeder.country.flag_css)
        else:
            return record.variety

    class Meta:
        model = SeedSample
        fields = ("sample_id", "variety", "position", "weight", "germinability", "growing_season", "notes", "actions")
        template_name = "collect/partials/seedsample_table.html"
        empty_text = "There are no corresponding seed samples to be displayed."
