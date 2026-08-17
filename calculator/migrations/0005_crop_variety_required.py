import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("calculator", "0004_crop_layouts_and_observations"),
    ]

    operations = [
        migrations.AlterField(
            model_name="crop",
            name="variety",
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to="register.plantvariety"),
        ),
    ]
