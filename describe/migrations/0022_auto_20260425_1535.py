# 0022_auto_20260425_1535.py
from django.db import migrations


def forward(apps, schema_editor):
    State = apps.get_model("describe", "State")
    StateGroup = apps.get_model("describe", "StateGroup")

    states = list(State.objects.prefetch_related("related_states").only("id"))

    visited = set()
    components = []

    for state in states:
        if state.id in visited:
            continue

        stack = [state]
        component_ids = []

        while stack:
            node = stack.pop()

            if node.id in visited:
                continue

            visited.add(node.id)
            component_ids.append(node.id)

            stack.extend(node.related_states.all())

        components.append(component_ids)

    groups = StateGroup.objects.bulk_create(
        [StateGroup() for _ in components],
        batch_size=1000,
    )

    states_to_update = []

    state_by_id = {state.id: state for state in states}

    for group, component_ids in zip(groups, components, strict=True):
        for state_id in component_ids:
            state = state_by_id[state_id]
            state.group_id = group.id
            states_to_update.append(state)

    State.objects.bulk_update(states_to_update, ["group"], batch_size=1000)


class Migration(migrations.Migration):
    dependencies = [
        ("describe", "0021_stategroup_state_group"),
    ]

    operations = [
        migrations.RunPython(forward, reverse_code=migrations.RunPython.noop),
    ]
