from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("spaces", "0004_remove_area_and_location_cols"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="location",
            name="order",
        ),
    ]
