from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("calculator", "0006_alter_croplayout_description_and_more"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="parameterobservation",
            options={"ordering": ("-recorded_at", "-pk")},
        ),
        migrations.AlterModelOptions(
            name="traitobservation",
            options={"ordering": ("-recorded_at", "-pk")},
        ),
    ]
