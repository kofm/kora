from django.apps import AppConfig
from django.db.models.signals import post_delete, post_save


class RegisterConfig(AppConfig):
    name = "register"

    def ready(self):
        from . import signals

        post_save.connect(signals.plantvarietyname_handler, sender="register.PlantVarietyName")
        post_delete.connect(signals.plantvarietyname_delete_handler, sender="register.PlantVarietyName")
        post_save.connect(signals.plantvariety_handler, sender="register.PlantVariety")
