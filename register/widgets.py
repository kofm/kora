from django.urls import reverse_lazy

from frontpage.widgets import ModelTomSelect, TomSelectConfig, TomSelectMultiple


class PlantSpeciesSelect(ModelTomSelect):
    ts_config = TomSelectConfig(
        url=reverse_lazy("register:plantspecies_autocomplete"),
        search_param="common_name__icontains",
        value_field="id",
        label_field="common_name",
        search_field="common_name",
        max_options=100,
        preload="true",
    )


class PlantSpeciesSelectMultiple(TomSelectMultiple):
    ts_config = TomSelectConfig(
        url=reverse_lazy("register:plantspecies_autocomplete"),
        search_param="common_name__icontains",
        value_field="id",
        label_field="common_name",
        search_field="common_name",
        max_options=100,
    )


class PlantVarietySelect(ModelTomSelect):
    ts_config = TomSelectConfig(
        url=reverse_lazy("register:variety_autocomplete"),
        search_param="name__icontains",
        value_field="id",
        label_field="name",
        search_field="name",
        depends_on="species",
        depends_param="species_id",
        disabled=True,
    )
