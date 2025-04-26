import django_tables2 as tables
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
