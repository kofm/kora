from frontpage.fields import RemoteModelChoiceField, RemoteModelMultipleChoiceField
from register.models import PlantSpecies, PlantVariety
from register.widgets import PlantSpeciesSelect, PlantSpeciesSelectMultiple, PlantVarietySelect


class PlantSpeciesChoiceField(RemoteModelChoiceField):
    model = PlantSpecies
    widget = PlantSpeciesSelect

    default_error_messages = {
        **RemoteModelMultipleChoiceField.default_error_messages,
        "invalid_choice": "Plant species do not exist: %(ids)s",
    }


class PlantSpeciesMultipleChoiceField(RemoteModelMultipleChoiceField):
    model = PlantSpecies
    widget = PlantSpeciesSelectMultiple

    default_error_messages = {
        **RemoteModelMultipleChoiceField.default_error_messages,
        "invalid_choice": "Plant species do not exist: %(ids)s",
    }


class PlantVarietyChoiceField(RemoteModelChoiceField):
    model = PlantVariety
    widget = PlantVarietySelect

    default_error_messages = {
        **RemoteModelMultipleChoiceField.default_error_messages,
        "invalid_choice": "Plant species do not exist: %(ids)s",
    }
