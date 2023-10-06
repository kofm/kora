from django.views.generic import CreateView
from register.models import PlantSpecies
from frontpage.decorators import NavActive, nav_active
from typing import List
from typing import Tuple


class NavActivePlants(NavActive):
    """A mixin for displaying the Plant menu item as selected."""

    def __init__(self) -> None:
        super().__init__("nav_plants")


# A decorator for displaying the Plant menu item as selected.
nav_active_plants = nav_active("nav_plants")


def custom_variety_crumbs(species: PlantSpecies, *args) -> List[Tuple[str, str]]:
    """This function builds the custom breadcrumbs used in PlantVariety views.
    Home / Plants / Species / ...
    """
    return [
        (str(species._meta.verbose_name_plural.capitalize()), species.get_list_url()),
        (str(species), species.get_absolute_url()),
        *args,
    ]


class PlantCreateMixin(NavActivePlants, CreateView):
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["object_to_create"] = self.model._meta.verbose_name.capitalize()
        return context
