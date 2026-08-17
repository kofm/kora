from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("parameters", "0007_alter_speciesparameter_options_and_more"),
    ]

    operations = [
        migrations.DeleteModel(name="SpeciesParameter"),
    ]
