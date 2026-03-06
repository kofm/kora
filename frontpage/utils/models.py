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


def copy_model_concrete_fields(src, dst, *, exclude=None, include=None):
    if src._meta.model != dst._meta.model:
        raise TypeError("src and dst must be instances of the same model")

    exclude = set(exclude or ())
    include = set(include) if include is not None else None

    for field in src._meta.concrete_fields:
        if field.primary_key:
            continue
        if not field.editable:
            continue

        name = field.name

        if name in exclude:
            continue
        if include is not None and name not in include:
            continue

        setattr(dst, name, getattr(src, name))

    return dst
