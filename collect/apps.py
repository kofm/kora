from django.apps import AppConfig
from django.db.models.signals import pre_save


class CollectConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "collect"

    def ready(self):
        from . import signals

        # Signal to make inactive, i.e. active=False, all the other user's Cart
        # instances when selecting a new Cart instance
        pre_save.connect(signals.unique_cart_active, sender="collect.Cart")
