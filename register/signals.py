from register.models import PlantSpecies, PlantVariety, PlantVarietyName
from django.db.models.signals import post_save
from django.dispatch import receiver

@receiver(post_save, sender=PlantVarietyName)
def plantvariety_handler(sender, instance, **kwargs):
    related_variety = PlantVariety.objects.get(pk=instance.variety.pk)
    related_variety.name = instance.name
    related_variety.save()
