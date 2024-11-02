from frontpage.decorators import NavActive, nav_active


class NavPlantActiveContext(NavActive):
    """A mixin for displaying the Plant menu item as selected."""

    def __init__(self) -> None:
        super().__init__("nav_plants")


# A decorator for displaying the Plant menu item as selected.
nav_active_plants = nav_active("nav_plants")
