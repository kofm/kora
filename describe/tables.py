import django_tables2 as tables
from django.utils.html import format_html

from describe.models import Description, Protocol, State

link_classes = "text-decoration-none link-body-emphasis"


class DescriptionTable(tables.Table):
    variety__name = tables.Column("Variety", linkify=True)
    actions = tables.TemplateColumn(
        template_name="describe/partials/description_table_actions.html",
        verbose_name="",
        orderable=False,
    )

    class Meta:
        model = Description
        fields = ("variety__name", "variety__species__latin_name", "name", "protocol__name")
        template_name = "describe/partials/description_table.html"


class RelatedStatesTable(tables.Table):
    actions = tables.TemplateColumn(
        template_name="describe/partials/relatedstate_table_actions.html",
        verbose_name="",
        orderable=False,
    )

    class Meta:
        model = State
        fields = ("numeric_id", "description", "trait", "trait__protocol")
