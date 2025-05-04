import django_tables2 as tables

from frontpage.tables import TableHoverFixed
from parameters.models import Parameter, SpeciesParameter, VarietalParameter


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
        fields = ("variety", "value", "note")
        empty_text = "There are no associated parameters."
        per_page = 15
        prefix = "vp"
        template_name = "frontpage/partials/htmx_table.html"


class SpeciesParameterTable(tables.Table):
    class Meta:
        model = SpeciesParameter
        fields = ("specie", "value", "note")
        empty_text = "There are no associated parameters."
        per_page = 15
        prefix = "sp"
        template_name = "frontpage/partials/htmx_table.html"
