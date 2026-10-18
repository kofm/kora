from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [("parameters", "0009_alter_varietalparameter_options")]

    operations = [
        migrations.AddField(
            model_name="parameter",
            name="type",
            field=models.CharField(
                max_length=7,
                default="decimal",
                choices=[
                    ("boolean", "Boolean"),
                    ("integer", "Integer"),
                    ("decimal", "Decimal"),
                    ("date", "Date"),
                    ("text", "Text"),
                ],
            ),
        ),
        migrations.AlterField(
            model_name="parameter",
            name="measure_unit",
            field=models.CharField(max_length=50, blank=True, help_text="The unit of measurement."),
        ),
        *[
            migrations.AddField(model_name="varietalparameter", name=name, field=field)
            for name, field in [
                ("value_boolean", models.BooleanField(null=True, blank=True)),
                ("value_integer", models.BigIntegerField(null=True, blank=True)),
                ("value_decimal", models.DecimalField(max_digits=20, decimal_places=10, null=True, blank=True)),
                ("value_date", models.DateField(null=True, blank=True)),
                ("value_text", models.TextField(null=True, blank=True)),
            ]
        ],
    ]
