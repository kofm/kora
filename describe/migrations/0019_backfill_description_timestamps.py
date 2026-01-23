from django.db import migrations
from django.utils import timezone


def backfill_timestamps(apps, schema_editor):
    Description = apps.get_model("describe", "Description")
    now = timezone.now()
    Description.objects.filter(created_at__isnull=True).update(created_at=now)
    Description.objects.filter(updated_at__isnull=True).update(updated_at=now)


class Migration(migrations.Migration):
    dependencies = [
        ("describe", "0018_description_created_at_description_notes_and_more"),
    ]

    operations = [
        migrations.RunPython(backfill_timestamps, migrations.RunPython.noop),
    ]
