from django.apps import AppConfig
from django.db.models.signals import post_save


class RegisterConfig(AppConfig):
    name = "register"
    def ready(self):
        from . import signals
        post_save.connect(signals.plantvariety_handler, sender='register.PlantVarietyName')
