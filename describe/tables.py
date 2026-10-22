import django_tables2 as tables
from django.utils.html import format_html

from describe.models import Description, State
from frontpage.tables import TableHoverFixed


class DescriptionTable(tables.Table):
    variety__name = tables.Column("Variety", attrs={"td": {"class": "fw-bold"}})
    variety__species__common_name = tables.Column("Species")
    protocol__name = tables.Column("Protocol")
    updated_at = tables.DateTimeColumn(verbose_name="Last updated", short=False, attrs={"td": {"class": "text-muted"}})
    actions = tables.TemplateColumn(
        template_name="describe/partials/description_table_actions.html",
        verbose_name="",
        orderable=False,
    )

    class Meta(TableHoverFixed.Meta):
        attrs = {"class": "table table-hover table-fixed small-table compact-table"}
        model = Description
        fields = ("variety__name", "variety__species__common_name", "label", "protocol__name", "updated_at")
        template_name = "describe/partials/description_table.html"
        per_page = 10
        empty_text = "There are no matching descriptions."

    def render_label(self, record, value):
        return format_html(
            '<span class="badge rounded-pill {} text-nowrap"><small>{}</small></span>',
            value.colour_class,
            value,
        )


class RelatedStatesTable(tables.Table):
    actions = tables.TemplateColumn(
        template_name="describe/partials/relatedstate_table_actions.html",
        verbose_name="",
        orderable=False,
    )

    class Meta:
        model = State
        fields = ("numeric_id", "description", "trait", "trait__protocol")
