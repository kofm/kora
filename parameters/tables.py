import django_tables2 as tables

from frontpage.tables import TableHoverFixed
from parameters.models import Parameter, VarietalParameter


class ParameterTable(tables.Table):
    class Meta(TableHoverFixed.Meta):
        model = Parameter
        exclude = ("id",)
        per_page = 10
        template_name = "frontpage/partials/htmx_table.html"


class VarietalParameterTable(tables.Table):
    actions = tables.TemplateColumn(
        template_name="parameters/partials/varietalparameter_table_actions.html",
        verbose_name="",
        orderable=False,
        attrs={"td": {"class": "text-end"}},
    )

    class Meta:
        model = VarietalParameter
        fields = ("variety__name", "parameter__name", "parameter__code", "value", "url_ref", "note")
        empty_text = "There are no associated parameters."
        per_page = 15
        template_name = "frontpage/partials/htmx_table.html"
        attrs = {"class": "table table-hover table-fixed"}
