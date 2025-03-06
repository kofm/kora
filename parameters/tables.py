import django_tables2 as tables

from parameters.models import Parameter, SpeciesParameter, VarietalParameter


class ParameterTable(tables.Table):
    code = tables.Column(linkify=True)
    actions = tables.TemplateColumn(
        template_name="parameters/partials/parameter_table_actions.html",
        verbose_name="",
        orderable=False,
        attrs={"td": {"class": "text-end"}},
    )

    class Meta:
        model = Parameter
        exclude = ("id",)


class VarietalParameterTable(tables.Table):
    actions = tables.TemplateColumn(
        template_name="parameters/partials/varietalparameter_table_actions.html",
        verbose_name="",
        orderable=False,
        attrs={"td": {"class": "text-end"}},
    )

    class Meta:
        model = VarietalParameter
        fields = ("variety", "value", "note", "created_at", "updated_at")
        empty_text = "There are no associated parameters."


class SpeciesParameterTable(tables.Table):
    class Meta:
        model = SpeciesParameter
        fields = ("specie", "value", "note", "created_at", "updated_at")
        empty_text = "There are no associated parameters."
