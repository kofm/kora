from typing import Any, Dict
from ..utils import CONTEXT_KEY


class CreateBreadcrumbsMixin:
    def get_context_data(self, *args: Any, **kwargs: Any) -> Dict[str, Any]:
        context = super().get_context_data(*args, **kwargs)
        context[CONTEXT_KEY] = [
            (
                self.model._meta.verbose_name_plural.capitalize(),
                f"{self.model._meta.app_label}:{self.model._meta.verbose_name}_list",
            ),
            ("Create", None),
        ]
        return context
