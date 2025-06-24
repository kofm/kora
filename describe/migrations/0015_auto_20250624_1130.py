from django.db import migrations


def fill_numeric_ids(apps, schema_editor):
    Trait = apps.get_model("describe", "Trait")
    from django.db.models import Max

    for protocol_id in Trait.objects.filter(numeric_id__isnull=True).values_list("protocol_id", flat=True).distinct():
        agg = Trait.objects.filter(protocol_id=protocol_id, numeric_id__isnull=False).aggregate(max=Max("numeric_id"))
        max_id = agg["max"] or 0

        for trait in Trait.objects.filter(protocol_id=protocol_id, numeric_id__isnull=True).order_by("pk"):
            max_id += 1
            trait.numeric_id = max_id
            trait.save(update_fields=["numeric_id"])


def no_op(apps, schema_editor):
    pass


class Migration(migrations.Migration):
    dependencies = [
        ("describe", "0014_alter_protocol_options"),
    ]

    operations = [
        migrations.RunPython(fill_numeric_ids, no_op),
    ]
