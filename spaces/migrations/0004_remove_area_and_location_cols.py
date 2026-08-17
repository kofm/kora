from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("calculator", "0004_crop_layouts_and_observations"),
        ("spaces", "0003_location_cols_alter_area_length_alter_area_name_and_more"),
    ]

    operations = [
        migrations.DeleteModel(name="Area"),
        migrations.RemoveField(model_name="location", name="cols"),
    ]
