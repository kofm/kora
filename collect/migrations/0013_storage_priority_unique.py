from django.db import migrations, models
from django.db.models import Deferrable


def normalize_storage_order(apps, schema_editor):
    Storage = apps.get_model("collect", "Storage")
    ids = Storage.objects.using(schema_editor.connection.alias).order_by("order", "pk").values_list("pk", flat=True)
    for order, pk in enumerate(ids.iterator()):
        Storage.objects.using(schema_editor.connection.alias).filter(pk=pk).update(order=order)


class Migration(migrations.Migration):
    dependencies = [("collect", "0012_storageposition_name_to_int")]

    operations = [
        migrations.RunPython(normalize_storage_order, migrations.RunPython.noop),
        migrations.AlterField(model_name="storage", name="order", field=models.PositiveIntegerField()),
        migrations.AlterModelOptions(
            name="storage", options={"ordering": ("order", "pk"), "verbose_name_plural": "storage"}
        ),
        migrations.AddConstraint(
            model_name="storage",
            constraint=models.UniqueConstraint(
                fields=("order",), name="unique_storage_priority", deferrable=Deferrable.DEFERRED
            ),
        ),
    ]
