from functools import wraps

from django.apps import apps
from django.contrib.auth import get_permission_codename
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from django.db.models import Model
from django.db.models.options import Options


def skip_if_not_app(app_name):
    def decorator(func):
        @wraps(func)
        def wrapper(sender, **kwargs):
            if sender.name != app_name:
                return
            return func(sender, **kwargs)

        return wrapper

    return decorator


def get_or_create_usergroups(app):
    viewers, _ = Group.objects.get_or_create(name=f"view_{app}")
    editors, _ = Group.objects.get_or_create(name=f"edit_{app}")
    return viewers, editors


def group_assign_model_permissions(app_label, model_name, group, actions=("view", "add", "change", "delete")):
    model = apps.get_model(app_label, model_name)
    content_type = ContentType.objects.get_for_model(model)
    name = model._meta.model_name
    for action in actions:
        codename = f"{action}_{name}"
        try:
            permission = Permission.objects.get(codename=codename, content_type=content_type)
            group.permissions.add(permission)
        except Permission.DoesNotExist:
            continue


def get_permission_from_opts(action: str, opts: Options) -> str:
    if not isinstance(opts, Options):
        raise TypeError(f"Expected Django model _meta (Options), got {type(opts).__name__}")
    app_label = opts.app_label
    codename = get_permission_codename(action, opts)
    return f"{app_label}.{codename}"


def get_permission_from_instance(action: str, instance: Model):
    opts = instance._meta
    return get_permission_from_opts(action, opts)
