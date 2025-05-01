from typing import override

from django.apps import AppConfig


class CollectConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "collect"

    def ready(self):
        from . import signals
