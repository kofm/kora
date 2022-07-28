import django_tables2 as tables

from describe.models import Description

class DescriptionTable(tables.Table):
    variety = tables.Column(
        linkify=True,
        attrs={
            "a": {"class": "text-decoration-none link-dark"},
            "th": {"class": "text-decoration-none link-dark"}
        }
    )
    name = tables.Column(
        linkify=True,
        attrs={"a": {"class": "text-decoration-none link-dark"}}
    )
    protocol = tables.Column(
        linkify=True,
        attrs={"a": {"class": "text-decoration-none link-dark"}}
    )
    class Meta:
        model = Description
        fields = ("variety", "name", "protocol")
