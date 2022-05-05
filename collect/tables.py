import django_tables2 as tables

from collect.models import SeedSample


class SeedSampleTable(tables.Table):
    variety = tables.Column(linkify=True)
    germinability = tables.Column(verbose_name="Germinability")
    weight = tables.Column(verbose_name="Weight (g)")

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
        self.columns['variety'].column.attrs = {"td":{"class" : "col-2" }}
        self.columns['notes'].column.attrs = {"td":{"class" : "col-3" }}

    def render_germinability(self, record):
        return str(record.germinability) + "%"

    def render_weight(self, record):
        return int(record.weight)

    class Meta:
        model = SeedSample
        fields = ("sample_id", "variety", "position", "weight", "germinability", "growing_season", "notes")
        template_name = "collect/partials/seedsample_table.html"
        empty_text = "There are no corresponding seed samples to be displayed."
