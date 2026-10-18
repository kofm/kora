from django.db import migrations, models

FIELDS = ("value_boolean", "value_integer", "value_decimal", "value_date", "value_text")


def exactly_one_value():
    condition = models.Q()
    for selected in FIELDS:
        condition |= models.Q(**{f"{field}__isnull": field != selected for field in FIELDS})
    return condition


class Migration(migrations.Migration):
    dependencies = [
        ("calculator", "0011_migrate_typed_values"),
        ("parameters", "0011_finalize_typed_values"),
    ]
    operations = [
        migrations.RemoveConstraint(model_name="parameterobservation", name="at_least_one_of_value_or_date"),
        migrations.RemoveField(model_name="cropparameter", name="value"),
        migrations.RemoveField(model_name="parameterobservation", name="parameter_value"),
        migrations.RemoveField(model_name="parameterobservation", name="parameter_date"),
        *[
            migrations.AddConstraint(
                model_name=model,
                constraint=models.CheckConstraint(condition=exactly_one_value(), name=f"calculator_{model}_one_value"),
            )
            for model in ("cropparameter", "parameterobservation")
        ],
    ]
