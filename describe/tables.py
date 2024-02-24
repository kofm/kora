from django.utils.html import format_html
import django_tables2 as tables

from describe.models import Description, State


class DescriptionTable(tables.Table):
    def render_expressions(self, record):
        return format_html(
            "{}/{}", record.expressions.count(), record.available_traits.count()
        )

    variety = tables.Column(
        linkify=True,
        attrs={
            "a": {"class": "text-decoration-none link-body-emphasis"},
            "th": {"class": "text-decoration-none link-body-emphasis"},
        },
    )
    name = tables.Column(
        linkify=True,
        attrs={
            "a": {"class": "text-decoration-none link-body-emphasis fw-bold"},
        },
    )
    protocol = tables.Column(
        linkify=True, attrs={"a": {"class": "text-decoration-none link-body-emphasis"}}
    )
    expressions = tables.Column("Expressions")
    actions = tables.TemplateColumn(
        template_name="describe/partials/description_table_actions.html",
        verbose_name="",
        orderable=False,
        attrs={"td": {"class": "col-1 text-end"}},
    )

    class Meta:
        model = Description
        fields = ("variety", "name", "protocol")


class RelatedStatesTable(tables.Table):
    actions = tables.TemplateColumn(
        template_name="describe/partials/relatedstate_table_actions.html",
        verbose_name="",
        orderable=False,
    )

    class Meta:
        model = State
        fields = ("numeric_id", "description", "trait", "trait__protocol")
