import django_tables2 as tables

from frontpage.tables import EditDeleteColumn, TableHoverFixed
from parameters.models import Parameter, VarietalParameter


class ParameterTable(tables.Table):
    code = tables.Column(attrs={"td": {"class": "fw-light"}})
    name = tables.Column(attrs={"td": {"class": "fw-bold"}})
    description = tables.Column(attrs={"td": {"class": "text-muted"}})

    actions = EditDeleteColumn()

    class Meta(TableHoverFixed.Meta):
        model = Parameter
        exclude = ("id",)
        per_page = 10
        template_name = "frontpage/partials/htmx_table.html"


class VarietalParameterTable(tables.Table):
    value = tables.Column(accessor="get_value_display", orderable=False)
    variety__name = tables.Column("Variety", attrs={"td": {"class": "fw-bold"}})
    parameter__name = tables.Column("Parameter", attrs={"td": {"class": "text-muted"}})
    note = tables.Column("Notes", attrs={"td": {"class": "fw-light"}})
    actions = EditDeleteColumn(preserve_next=True)

    class Meta:
        model = VarietalParameter
        fields = ("variety__name", "parameter__code", "parameter__name", "value", "note")
        empty_text = "There are no associated parameters."
        per_page = 15
        template_name = "frontpage/partials/htmx_table.html"
        attrs = {"class": "table table-hover table-fixed small-table"}
