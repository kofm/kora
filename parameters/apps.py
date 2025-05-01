from typing import override

from django.apps import AppConfig


class ParametersConfig(AppConfig):
    name = "parameters"

    @override
    def ready(self):
        from . import signals
