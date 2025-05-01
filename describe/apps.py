from django.apps import AppConfig


class DescribeConfig(AppConfig):
    name = "describe"

    def ready(self):
        from . import signals
