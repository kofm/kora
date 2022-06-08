import django_tables2 as tables
from django_tables2 import columns
from django.utils.html import format_html

from register.models import Entity, Protection

class CountryRenderer:
    def render_country(self, record):
        return format_html('<i class="{}"></i>', record.country.flag_css)

class ProtectionTable(tables.Table, CountryRenderer):
    type = tables.Column(linkify=True)
    class Meta:
        model = Protection
        template_name = "django_tables2/bootstrap4.html"
        exclude = ('id', 'variety', )


class EntityTable(tables.Table, CountryRenderer):
    name = columns.Column(linkify=True)
    class Meta:
      model = Entity
      fields = ['name', 'country', 'email' ]

class PlantVarietyEntityTable(tables.Table):
    name = tables.Column(linkify=True)
    country = tables.TemplateColumn("<i class='{{ record.protection_set.last.country.flag_css }}'></i>", verbose_name="Country")
    class Meta:
        model = Entity
        fields = ['name', 'species', 'country']
