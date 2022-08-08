from django.utils.html import format_html
import django_tables2 as tables

from describe.models import Description, State

class DescriptionTable(tables.Table):
    variety = tables.Column(
        linkify=True,
        attrs={
            "a": {"class": "text-decoration-none link-dark"},
            "th": {"class": "text-decoration-none link-dark"}
        }
    )
    name = tables.Column(
        linkify=True,
        attrs={"a": {"class": "text-decoration-none link-dark"}}
    )
    protocol = tables.Column(
        linkify=True,
        attrs={"a": {"class": "text-decoration-none link-dark"}}
    )
    class Meta:
        model = Description
        fields = ("variety", "name", "protocol")

class RelatedStatesTable(tables.Table):
    actions = tables.TemplateColumn(
        template_name="describe/partials/relatedstate_table_actions.html",
        verbose_name="",
        orderable=False
    )
    class Meta:
        model = State
        fields = ("numeric_id", "description", "trait", "trait__protocol")
