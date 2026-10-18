from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("parameters", "0010_typed_value_columns"),
        ("calculator", "0009_alter_parametertarget_required_count_and_more"),
    ]

    operations = [
        migrations.AddField(model_name=model, name=name, field=field)
        for model in ("cropparameter", "parameterobservation")
        for name, field in [
            ("value_boolean", models.BooleanField(null=True, blank=True)),
            ("value_integer", models.BigIntegerField(null=True, blank=True)),
            ("value_decimal", models.DecimalField(max_digits=20, decimal_places=10, null=True, blank=True)),
            ("value_date", models.DateField(null=True, blank=True)),
            ("value_text", models.TextField(null=True, blank=True)),
        ]
    ]
