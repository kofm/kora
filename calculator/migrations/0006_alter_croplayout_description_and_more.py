import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("calculator", "0005_crop_variety_required"),
        ("spaces", "0004_remove_area_and_location_cols"),
    ]

    operations = [
        migrations.AlterField(
            model_name="croplayout",
            name="description",
            field=models.TextField(blank=True, default="Additional information about the layout"),
        ),
        migrations.AlterField(
            model_name="croplayout",
            name="location",
            field=models.ForeignKey(
                help_text="The location to which the layout belongs",
                on_delete=django.db.models.deletion.PROTECT,
                related_name="crop_layouts",
                to="spaces.location",
            ),
        ),
        migrations.AlterField(
            model_name="croplayout",
            name="name",
            field=models.CharField(help_text="A descriptive name for the layout", max_length=100),
        ),
        migrations.AlterField(
            model_name="croplayout",
            name="ncol",
            field=models.PositiveIntegerField(
                default=1, help_text="The number of columns in which crops are arranged", verbose_name="Columns"
            ),
        ),
        migrations.AlterField(
            model_name="croplayout",
            name="description",
            field=models.TextField(blank=True, default="", help_text="Additional information about the layout"),
        ),
    ]
