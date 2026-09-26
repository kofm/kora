from decimal import Decimal

import django_tables2 as tables
from django.utils.html import format_html

from frontpage.tables import TableHoverFixed
from spaces.models import Location


class LocationTable(tables.Table):
    coordinates = tables.Column("Coordinates")

    class Meta(TableHoverFixed.Meta):
        model = Location
        fields = ("name",)
        order_by = "name"
        template_name = "frontpage/partials/htmx_table.html"
        empty_text = "There are no locations to be displayed."

    def render_coordinates(self, value, record):
        lat = record.latitude
        lon = record.longitude

        return format_html(
            '<a class="row-link" '
            'href="https://www.openstreetmap.org/?mlat={}&mlon={}#map=15/{}/{}" '
            'target="_blank" rel="noopener noreferrer">{}, {}</a>',
            lat,
            lon,
            lat,
            lon,
            f"{Decimal(str(lat)):.4f}",
            f"{Decimal(str(lon)):.4f}",
        )
