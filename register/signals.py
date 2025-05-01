from webbrowser import get

from django.db.models.signals import post_delete, post_migrate, post_save
from django.dispatch import receiver

from frontpage.utils.permissions import (
    get_or_create_usergroups,
    group_assign_model_permissions,
    skip_if_not_app,
)
from register.models import PlantVariety, PlantVarietyName


@receiver(post_migrate)
@skip_if_not_app("register")
def setup_register_groups_and_permissions(sender, **kwargs):
    app_label = "register"
    viewers, editors = get_or_create_usergroups(app_label)
    for model_name in ("Entity", "PlantSpecies", "PlantVariety", "PlantVarietyName", "Protection"):
        group_assign_model_permissions(app_label, model_name, viewers, ("view",))
        group_assign_model_permissions(app_label, model_name, editors)


@receiver(post_save, sender=PlantVarietyName)
def plantvarietyname_handler(sender, instance, **kwargs):
    # Check if there's any newer name for this variety
    newer_name_exists = PlantVarietyName.objects.filter(
        variety=instance.variety, change_date__gt=instance.change_date
    ).exists()

    if not newer_name_exists:
        instance.variety.name = instance.name
        instance.variety.save()


@receiver(post_delete, sender=PlantVarietyName)
def plantvarietyname_delete_handler(sender, instance, **kwargs):
    related_variety = instance.variety
    if related_variety.names.exists():
        newest_name = related_variety.names.order_by("-change_date").first()
        related_variety.name = newest_name.name
        related_variety.save()


@receiver(post_save, sender=PlantVariety)
def plantvariety_handler(sender, instance, created, **kwargs):
    if created:
        plantvariety_name = PlantVarietyName(variety=instance, name=instance.name)
        plantvariety_name.save()
