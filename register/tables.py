from django.utils.safestring import mark_safe
import django_tables2 as tables
from django_tables2 import columns
from django.utils.html import format_html
from collect.models import SeedSample
from describe.models import Description

from parameters.models import VarietalParameter

from register.models import Entity, PlantVariety, Protection

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

def render_icon(value):
    if value:
        icon = "bi-check"
    else:
        icon = "bi-dash"
    return format_html('<i class="bi {}"></i>', icon)

class PlantVarietyTable(tables.Table):
    name = tables.Column(linkify=True)
    described = tables.Column(empty_values=(), verbose_name="Described", orderable=False)
    accessions = tables.Column(empty_values=(), verbose_name="Accessions", orderable=False)

    class Meta:
        model = PlantVariety
        fields = ('name', 'breeder', 'created_at')


    def render_protected(self, record):
        protected = Protection.objects.filter(variety=record, type="PBR", status="G").exists()
        return render_icon(protected)

    def render_enlisted(self, record):
        enlisted = Protection.objects.filter(variety=record, type__in=["CAT", "NLI"], status="G").exists()
        return render_icon(enlisted)

    def render_described(self, record):
        described = Description.objects.filter(variety=record).exists()
        return render_icon(described)


    def render_accessions(self, record):
        accessions = SeedSample.objects.filter(variety=record).exists()
        return render_icon(accessions)
