from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("describe", "0010_alter_state_options_alter_trait_protocol"),
    ]

    operations = [
        migrations.RenameModel(
            old_name="DescriptionsUserList",
            new_name="Workspace",
        ),
        migrations.RenameModel(
            old_name="DescriptionsUserListElement",
            new_name="WorkspaceElement",
        ),
    ]
