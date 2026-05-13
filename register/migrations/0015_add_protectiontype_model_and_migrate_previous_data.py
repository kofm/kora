import django.db.models.deletion
from django.db import migrations, models

PROTECTION_TYPES = {
    "PBR": "Plant Breeders' Rights",
    "NLI": "National Listing",
    "CAT": "Common Catalogue",
}


def forwards(apps, schema_editor):
    Protection = apps.get_model("register", "Protection")
    ProtectionType = apps.get_model("register", "ProtectionType")

    type_by_code = {}

    for code, name in PROTECTION_TYPES.items():
        protection_type, _ = ProtectionType.objects.update_or_create(
            code=code,
            defaults={"name": name},
        )
        type_by_code[code] = protection_type

    for code, protection_type in type_by_code.items():
        Protection.objects.filter(type=code).update(protection_type_id=protection_type.pk)

    unmapped = Protection.objects.filter(protection_type__isnull=True).values_list("type", flat=True).distinct()

    unmapped = list(unmapped)

    if unmapped:
        raise ValueError(f"Some Protection.type values could not be mapped to ProtectionType: {unmapped}")


class Migration(migrations.Migration):
    dependencies = [
        ("register", "0014_alter_entity_email"),
    ]

    operations = [
        migrations.CreateModel(
            name="ProtectionType",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("code", models.CharField(max_length=3, unique=True)),
                ("name", models.CharField(max_length=100)),
            ],
            options={
                "ordering": ["code"],
            },
        ),
        migrations.AddField(
            model_name="protection",
            name="protection_type",
            field=models.ForeignKey(
                to="register.protectiontype",
                on_delete=django.db.models.deletion.PROTECT,
                null=True,
                blank=True,
            ),
        ),
        migrations.RunPython(forwards, reverse_code=migrations.RunPython.noop),
    ]
