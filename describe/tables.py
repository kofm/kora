import django_tables2 as tables
from django.utils.html import format_html

from describe.models import Description, State
from frontpage.tables import TableHoverFixed

link_classes = "text-decoration-none link-body-emphasis"


class DescriptionTable(tables.Table):
    variety__name = tables.Column("Variety")
    variety__species__common_name = tables.Column("Species")
    protocol__name = tables.Column("Protocol", attrs={"td": {"class": "text-nowrap text-truncate"}})
    actions = tables.TemplateColumn(
        template_name="describe/partials/description_table_actions.html",
        verbose_name="",
        orderable=False,
    )

    class Meta(TableHoverFixed.Meta):
        model = Description
        fields = ("variety__name", "variety__species__common_name", "name", "protocol__name")
        template_name = "describe/partials/description_table.html"

    def render_name(self, record, value):
        return format_html(f'<span class="badge rounded-pill text-bg-info">{value}</span>')


class RelatedStatesTable(tables.Table):
    actions = tables.TemplateColumn(
        template_name="describe/partials/relatedstate_table_actions.html",
        verbose_name="",
        orderable=False,
    )

    class Meta:
        model = State
        fields = ("numeric_id", "description", "trait", "trait__protocol")
