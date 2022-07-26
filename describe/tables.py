import django_tables2 as tables

from describe.models import Description

class DescriptionTable(tables.Table):
    variety = tables.Column(linkify=True)
    name = tables.Column(linkify=True)
    protocol = tables.Column(linkify=True)
    class Meta:
        model = Description
        fields = ("variety", "name", "protocol")
