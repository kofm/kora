from django.db.models.signals import post_delete, post_save
from django.dispatch import receiver

from register.models import PlantVariety, PlantVarietyName


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
