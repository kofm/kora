import django_tables2 as tables
from django.utils.html import format_html

from describe.models import Description, Protocol, State


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
    name = tables.Column(linkify=True, attrs={"a": {"class": "text-decoration-none link-body-emphasis fw-bold"}})
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
        template_name = "frontpage/partials/table.html"


class RelatedStatesTable(tables.Table):
    actions = tables.TemplateColumn(
        template_name="describe/partials/relatedstate_table_actions.html",
        verbose_name="",
        orderable=False,
    )

    class Meta:
        model = State
        fields = ("numeric_id", "description", "trait", "trait__protocol")


class ProtocolTable(tables.Table):
    name = tables.Column(linkify=True)

    def render_url_ref(self, record):
        return format_html('<i class="bi bi-link-45deg"></i>')

    class Meta:
        model = Protocol
        fields = ("name", "plantspecies", "url_ref")
