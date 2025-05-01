from functools import wraps

from django.apps import apps
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType


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
