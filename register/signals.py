from django.db.models.signals import post_delete, post_save
from django.dispatch import receiver

from register.models import PlantVariety, PlantVarietyName


@receiver(post_save, sender=PlantVarietyName)
def plantvarietyname_handler(sender, instance, **kwargs):
    related_variety = PlantVariety.objects.get(pk=instance.variety.pk)
    related_variety.name = instance.name
    related_variety.save()


@receiver(post_delete, sender=PlantVarietyName)
def plantvarietyname_delete_handler(sender, instance, **kwargs):
    related_variety = instance.variety
    other_names = related_variety.names.all()
    if other_names.exists():
        related_variety.name = other_names.last().name
        related_variety.save()


@receiver(post_save, sender=PlantVariety)
def plantvariety_handler(sender, instance, created, **kwargs):
    if created:
        plantvariety_name = PlantVarietyName(variety=instance, name=instance.name)
        plantvariety_name.save()
