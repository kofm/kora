from django.utils.html import format_html
import django_tables2 as tables

from describe.models import Description, State


class DescriptionTable(tables.Table):
    def render_expressions(self, record):
        expressions = record.expressions.count()
        traits = record.available_traits.count()
        color = "success" if expressions == traits else "secondary"
        return format_html('<span class="badge rounded-pill text-bg-{}">{}/{}</span>', color, expressions, traits)

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
    protocol__name = tables.Column(
        "Protocol", linkify=True, attrs={"a": {"class": "text-decoration-none link-body-emphasis"}}
    )
    expressions = tables.Column("Expressions", attrs={"td": {"class": "col-1 text-end"}})
    actions = tables.TemplateColumn(
        template_name="describe/partials/description_table_actions.html",
        verbose_name="",
        orderable=False,
        attrs={"td": {"class": "col-1 text-end"}},
    )

    class Meta:
        model = Description
        fields = ("variety", "name", "protocol__name")


class RelatedStatesTable(tables.Table):
    actions = tables.TemplateColumn(
        template_name="describe/partials/relatedstate_table_actions.html",
        verbose_name="",
        orderable=False,
    )

    class Meta:
        model = State
        fields = ("numeric_id", "description", "trait", "trait__protocol")
