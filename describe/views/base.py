from typing_extensions import List, Tuple
from frontpage.decorators import NavActive

from register.models import PlantSpecies


def custom_variety_crumbs(species: PlantSpecies, *args) -> List[Tuple[str, str]]:
    """Build the custom breadcrumbs used in PlantVariety views.

    Home / Plants / Species / ...
    """
    return [
        (str(species._meta.verbose_name_plural.capitalize()), species.get_list_url()),
        (str(species), species.get_absolute_url()),
        *args,
    ]

class NavActiveDescribe(NavActive):
    """Class for displaying active navigation in UI for Describe section."""

    def __init__(self) -> None:
        """Initialize the `nav` as 'nav_describe'."""
        super().__init__("nav_describe")
