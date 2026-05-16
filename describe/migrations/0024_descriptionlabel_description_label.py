import django.db.models.deletion
from django.db import migrations, models

import frontpage.generic


class Migration(migrations.Migration):
    dependencies = [
        ("describe", "0023_alter_state_group_alter_state_related_states"),
    ]

    operations = [
        migrations.CreateModel(
            name="DescriptionLabel",
            fields=[
                ("id", models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("name", models.CharField(max_length=64, unique=True)),
                (
                    "colour",
                    models.CharField(
                        choices=[
                            ("gray", "Gray"),
                            ("blue", "Blue"),
                            ("indigo", "Indigo"),
                            ("purple", "Purple"),
                            ("pink", "Pink"),
                            ("teal", "Teal"),
                            ("cyan", "Cyan"),
                            ("green", "Green"),
                            ("amber", "Amber"),
                            ("brown", "Brown"),
                        ],
                        default="gray",
                        max_length=16,
                    ),
                ),
            ],
            bases=(frontpage.generic.ModelIsDeletableMixin, models.Model),
        ),
        migrations.AddField(
            model_name="description",
            name="label",
            field=models.ForeignKey(
                blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to="describe.descriptionlabel"
            ),
        ),
    ]
