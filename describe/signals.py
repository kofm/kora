from django.db.models.signals import post_migrate
from django.dispatch import receiver

from frontpage.utils.permissions import (
    get_or_create_usergroups,
    group_assign_model_permissions,
    skip_if_not_app,
)


@receiver(post_migrate)
@skip_if_not_app("describe")
def setup_register_groups_and_permissions(sender, **kwargs):
    app_label = "describe"

    viewers, editors = get_or_create_usergroups(app_label)
    for model_name in ("Protocol", "Description", "Trait", "State", "Expression"):
        group_assign_model_permissions(app_label, model_name, viewers, ("view",))
        group_assign_model_permissions(app_label, model_name, editors)

    for model_name in ("Workspace", "WorkspaceElement"):
        group_assign_model_permissions(app_label, model_name, editors)
