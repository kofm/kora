from decimal import Decimal, InvalidOperation

from django.db import migrations


def decimal_value(value, label):
    result = Decimal(str(value))
    try:
        fits = (
            result.is_finite()
            and abs(result) < Decimal("10000000000")
            and result == result.quantize(Decimal("0.0000000001"))
        )
    except InvalidOperation:
        fits = False
    if not fits:
        raise RuntimeError(
            f"{label}: {value!r} cannot fit decimal(20, 10) without rounding. Correct it before migrating."
        )
    return result


def migrate_values(apps, schema_editor):
    alias = schema_editor.connection.alias
    Parameter = apps.get_model("parameters", "Parameter")
    Reference = apps.get_model("parameters", "VarietalParameter")
    CropValue = apps.get_model("calculator", "CropParameter")
    Observation = apps.get_model("calculator", "ParameterObservation")
    Target = apps.get_model("calculator", "ParameterTarget")
    FieldBook = apps.get_model("calculator", "FieldBook")

    # Validate the entire dataset before creating companions or changing any rows.
    numeric_ids = set()
    date_ids = set()
    for Model, field in ((Reference, "value"), (CropValue, "value"), (Observation, "parameter_value")):
        for pk, parameter_id, value in Model.objects.using(alias).values_list("pk", "parameter_id", field).iterator():
            if value is not None:
                decimal_value(value, f"{Model._meta.label} #{pk}")
                numeric_ids.add(parameter_id)
    for pk, parameter_id, number, date in (
        Observation.objects.using(alias)
        .values_list("pk", "parameter_id", "parameter_value", "parameter_date")
        .iterator()
    ):
        if number is None and date is None:
            raise RuntimeError(f"ParameterObservation #{pk} has no value. Correct it before migrating.")
        if date is not None:
            date_ids.add(parameter_id)

    companions = {}
    codes = set(Parameter.objects.using(alias).values_list("code", flat=True))
    for parameter in Parameter.objects.using(alias).order_by("pk").iterator():
        if parameter.pk in date_ids and parameter.pk not in numeric_ids:
            Parameter.objects.using(alias).filter(pk=parameter.pk).update(type="date", measure_unit="")
        elif parameter.pk in date_ids:
            suffix = "_date"
            code = parameter.code[: 50 - len(suffix)] + suffix
            counter = 2
            while code in codes:
                suffix = f"_date_{counter}"
                code = parameter.code[: 50 - len(suffix)] + suffix
                counter += 1
            codes.add(code)
            companion = Parameter.objects.using(alias).create(
                code=code,
                name=parameter.name[:193] + " (date)",
                description=parameter.description,
                measure_unit="",
                type="date",
            )
            companions[parameter.pk] = companion.pk

    for Model in (Reference, CropValue):
        for row in Model.objects.using(alias).all().iterator():
            Model.objects.using(alias).filter(pk=row.pk).update(
                value_decimal=decimal_value(row.value, f"{Model._meta.label} #{row.pk}")
            )

    # Snapshot IDs: newly split observations must not be processed again.
    observation_ids = list(Observation.objects.using(alias).values_list("pk", flat=True))
    for pk in observation_ids:
        row = Observation.objects.using(alias).get(pk=pk)
        if row.parameter_value is not None:
            Observation.objects.using(alias).filter(pk=pk).update(
                value_decimal=decimal_value(row.parameter_value, f"ParameterObservation #{pk}")
            )
        if row.parameter_date is not None:
            date_parameter_id = companions.get(row.parameter_id, row.parameter_id)
            if row.parameter_value is None:
                Observation.objects.using(alias).filter(pk=pk).update(
                    parameter_id=date_parameter_id, value_date=row.parameter_date
                )
            else:
                Observation.objects.using(alias).create(
                    parameter_id=date_parameter_id,
                    value_date=row.parameter_date,
                    parameter_date=row.parameter_date,
                    parameter_value=None,
                    crop_id=row.crop_id,
                    step_id=row.step_id,
                    recorded_at=row.recorded_at,
                    created_by_id=row.created_by_id,
                    notes=row.notes,
                )

    for original_id, companion_id in companions.items():
        for target in Target.objects.using(alias).filter(parameter_id=original_id).iterator():
            Target.objects.using(alias).get_or_create(
                step_id=target.step_id,
                parameter_id=companion_id,
                defaults={"required_count": target.required_count},
            )

    for fieldbook in FieldBook.objects.using(alias).all().iterator():
        config = fieldbook.display_config
        if isinstance(config, dict) and config.get("model") == "parameter":
            config = dict(config)
            if config.get("field") == "date":
                config["id"] = companions.get(config["id"], config["id"])
            config["field"] = "value"
            FieldBook.objects.using(alias).filter(pk=fieldbook.pk).update(display_config=config)


class Migration(migrations.Migration):
    dependencies = [("calculator", "0010_typed_value_columns")]
    operations = [migrations.RunPython(migrate_values)]
