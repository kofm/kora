from django.db import migrations, models

FIELDS = ("value_boolean", "value_integer", "value_decimal", "value_date", "value_text")


def exactly_one_value():
    condition = models.Q()
    for selected in FIELDS:
        condition |= models.Q(**{f"{field}__isnull": field != selected for field in FIELDS})
    return condition


class Migration(migrations.Migration):
    dependencies = [
        ("parameters", "0010_typed_value_columns"),
        ("calculator", "0011_migrate_typed_values"),
    ]
    operations = [
        migrations.RemoveField(model_name="varietalparameter", name="value"),
        migrations.AddConstraint(
            model_name="varietalparameter",
            constraint=models.CheckConstraint(
                condition=exactly_one_value(), name="parameters_varietalparameter_one_value"
            ),
        ),
    ]
