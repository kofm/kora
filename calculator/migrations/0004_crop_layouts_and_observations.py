import django.db.models.deletion
import django.utils.timezone
from django.conf import settings
from django.db import migrations, models


def delete_obsolete_data(apps, schema_editor):
    Management = apps.get_model("calculator", "Management")
    Crop = apps.get_model("calculator", "Crop")
    Area = apps.get_model("spaces", "Area")

    Management.objects.all().delete()
    Crop.objects.all().delete()
    Area.objects.all().delete()


class Migration(migrations.Migration):
    dependencies = [
        ("calculator", "0003_alter_cropparameter_url_ref"),
        ("describe", "0017_alter_trait_unique_numeric_id_per_protocol"),
        ("parameters", "0007_alter_speciesparameter_options_and_more"),
        ("register", "0013_alter_plantspecies_options_and_more"),
        ("spaces", "0003_location_cols_alter_area_length_alter_area_name_and_more"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="CropLayout",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("name", models.CharField(max_length=100)),
                ("description", models.TextField(blank=True, default="")),
                ("ncol", models.PositiveIntegerField(default=1)),
                ("archived_at", models.DateTimeField(blank=True, null=True)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                (
                    "location",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name="crop_layouts",
                        to="spaces.location",
                    ),
                ),
            ],
            options={"ordering": ("name", "pk")},
        ),
        migrations.AddConstraint(
            model_name="croplayout",
            constraint=models.CheckConstraint(condition=models.Q(("ncol__gt", 0)), name="crop_layout_ncol_positive"),
        ),
        migrations.RunPython(delete_obsolete_data, migrations.RunPython.noop),
        migrations.RemoveField(model_name="management", name="crop"),
        migrations.RemoveField(model_name="crop", name="area"),
        migrations.RemoveField(model_name="crop", name="species"),
        migrations.AddField(
            model_name="management",
            name="layout",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="managements",
                to="calculator.croplayout",
            ),
        ),
        migrations.AddField(
            model_name="crop",
            name="layout",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.PROTECT,
                related_name="crops",
                to="calculator.croplayout",
            ),
        ),
        migrations.AddField(model_name="crop", name="order", field=models.PositiveIntegerField(default=0)),
        migrations.AddField(model_name="crop", name="created_at", field=models.DateTimeField(auto_now_add=True)),
        migrations.AddField(model_name="crop", name="updated_at", field=models.DateTimeField(auto_now=True)),
        migrations.AlterField(
            model_name="crop",
            name="variety",
            field=models.ForeignKey(
                blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to="register.plantvariety"
            ),
        ),
        migrations.AlterField(
            model_name="crop",
            name="notes",
            field=models.CharField(blank=True, default="", help_text="Notes relative to the Crop", max_length=500),
        ),
        migrations.AlterField(model_name="management", name="notes", field=models.TextField(blank=True, default="")),
        migrations.AlterField(
            model_name="managementtype", name="description", field=models.TextField(blank=True, default="")
        ),
        migrations.AlterModelOptions(name="crop", options={"ordering": ("order", "pk")}),
        migrations.CreateModel(
            name="FieldBook",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("name", models.CharField(max_length=200)),
                ("display_config", models.JSONField(null=True)),
                (
                    "layout",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name="fieldbooks",
                        to="calculator.croplayout",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Step",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("order", models.PositiveIntegerField(default=0)),
                (
                    "crop",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, related_name="steps", to="calculator.crop"
                    ),
                ),
                (
                    "fieldbook",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="steps",
                        to="calculator.fieldbook",
                    ),
                ),
            ],
            options={"ordering": ("order",), "unique_together": {("fieldbook", "crop")}},
        ),
        migrations.CreateModel(
            name="ParameterTarget",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("required_count", models.PositiveSmallIntegerField(default=1)),
                (
                    "parameter",
                    models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to="parameters.parameter"),
                ),
                (
                    "step",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="%(class)s",
                        to="calculator.step",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="TraitTarget",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("required_count", models.PositiveSmallIntegerField(default=1)),
                (
                    "step",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="%(class)s",
                        to="calculator.step",
                    ),
                ),
                ("trait", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to="describe.trait")),
            ],
        ),
        migrations.AddConstraint(
            model_name="parametertarget",
            constraint=models.UniqueConstraint(fields=("step", "parameter"), name="unique_parameter_target_per_step"),
        ),
        migrations.AddConstraint(
            model_name="traittarget",
            constraint=models.UniqueConstraint(fields=("step", "trait"), name="unique_trait_target_per_step"),
        ),
        migrations.CreateModel(
            name="TraitObservation",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("recorded_at", models.DateTimeField(default=django.utils.timezone.now)),
                ("notes", models.CharField(blank=True, default="", max_length=255)),
                (
                    "created_by",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name="%(class)s",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    "crop",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name="%(class)s",
                        to="calculator.crop",
                    ),
                ),
                ("state", models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to="describe.state")),
                (
                    "step",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="%(class)s",
                        to="calculator.step",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="ParameterObservation",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("recorded_at", models.DateTimeField(default=django.utils.timezone.now)),
                ("notes", models.CharField(blank=True, default="", max_length=255)),
                ("parameter_value", models.DecimalField(blank=True, decimal_places=3, max_digits=10, null=True)),
                ("parameter_date", models.DateField(blank=True, null=True)),
                (
                    "created_by",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name="%(class)s",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    "crop",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name="%(class)s",
                        to="calculator.crop",
                    ),
                ),
                (
                    "parameter",
                    models.ForeignKey(
                        null=False, on_delete=django.db.models.deletion.PROTECT, to="parameters.parameter"
                    ),
                ),
                (
                    "step",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="%(class)s",
                        to="calculator.step",
                    ),
                ),
            ],
        ),
        migrations.AddConstraint(
            model_name="parameterobservation",
            constraint=models.CheckConstraint(
                condition=models.Q(
                    ("parameter_value__isnull", False), ("parameter_date__isnull", False), _connector="OR"
                ),
                name="at_least_one_of_value_or_date",
            ),
        ),
    ]
