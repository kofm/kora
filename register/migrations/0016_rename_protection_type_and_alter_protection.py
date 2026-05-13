import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("register", "0015_add_protectiontype_model_and_migrate_previous_data"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="protection",
            name="type",
        ),
        migrations.RenameField(
            model_name="protection",
            old_name="protection_type",
            new_name="type",
        ),
        migrations.AlterField(
            model_name="protection",
            name="type",
            field=models.ForeignKey(
                to="register.protectiontype",
                on_delete=django.db.models.deletion.PROTECT,
            ),
        ),
    ]
