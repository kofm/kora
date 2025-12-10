from django.apps import apps
from django.db.models import Model


def model_from_label(label: str) -> type[Model]:
    """Resolve a Django model from 'app_label.ModelName' or 'app_label.modelname'."""
    try:
        app_label, model_name = label.split(".", 1)
    except ValueError as exc:
        raise ValueError(f"Invalid model label '{label}'. Expected format 'app_label.ModelName'.") from exc

    model = apps.get_model(app_label, model_name)
    if model is None:
        raise LookupError(f"No model found for label '{label}'.")
    return model
