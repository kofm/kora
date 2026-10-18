import django_tables2 as tables
from django.contrib.auth.models import User
from django.template.loader import render_to_string
from django.utils.html import format_html


class EditDeleteColumn(tables.Column):
    """Standard modal actions for models implementing ModelIsDeletableMixin and URL helpers."""

    empty_values = ()

    def __init__(self):
        super().__init__(verbose_name="", orderable=False, attrs={"td": {"class": "text-end"}})

    def render(self, record, table):
        user = table.request.user
        opts = record._meta
        return render_to_string(
            "frontpage/partials/edit_delete_column.html",
            {
                "record": record,
                "update_url": record.get_update_url(),
                "delete_url": record.get_delete_url(),
                "can_edit": user.has_perm(f"{opts.app_label}.change_{opts.model_name}"),
                "can_delete": user.has_perm(f"{opts.app_label}.delete_{opts.model_name}"),
            },
        )


class TableHoverFixed(tables.Table):
    class Meta:
        attrs = {"class": "table table-hover table-fixed small-table"}
        row_attrs = {
            "_": lambda record: format_html(
                "on click[event.target.closest('.row-action, .row-link') == null] go to url '{}'",
                record.get_absolute_url() if hasattr(record, "get_absolute_url") else "",
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
