import django_tables2 as tables
from django.contrib.auth.models import User
from django.utils.html import format_html


class TableHoverFixed(tables.Table):
    class Meta:
        attrs = {"class": "table table-hover table-fixed"}
        row_attrs = {
            "_": lambda record: format_html(
                "on click[event.target.closest('.row-action') == null] go to url '{}'", record.get_absolute_url()
            ),
            "role": "button",
        }


class UserTable(tables.Table):
    username = tables.TemplateColumn(template_name="frontpage/partials/username_column.html")
    actions = tables.TemplateColumn(template_name="frontpage/partials/user_table_actions.html", verbose_name="")

    class Meta:
        model = User
        fields = (
            "username",
            "first_name",
            "last_name",
            "is_staff",
            "is_superuser",
            "is_active",
            "actions",
        )
        template_name = "frontpage/partials/htmx_table.html"
        per_page = 10
