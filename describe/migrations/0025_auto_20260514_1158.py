from django.db import migrations


def normalise_name(name):
    return name.strip().capitalize()


def copy_names_to_tags(apps, schema_editor):
    Description = apps.get_model("describe", "Description")
    DescriptionLabel = apps.get_model("describe", "DescriptionLabel")

    names = Description.objects.order_by("name").values_list("name", flat=True).distinct()

    for name in names:
        label, _ = DescriptionLabel.objects.get_or_create(name=normalise_name(name))
        Description.objects.filter(name=name).update(label=label.pk)


class Migration(migrations.Migration):
    dependencies = [
        ("describe", "0024_descriptionlabel_description_label"),
    ]

    operations = [
        migrations.RunPython(copy_names_to_tags, reverse_code=migrations.RunPython.noop),
    ]
