"""Project-wide decorators."""


def nav_active(nav: str):
    """Add active menu item to view context.

    nav: The name of the navigation section that is currently active.

    """

    def decorator(view_func):
        def wrapper(request, *args, **kwargs):
            response = view_func(request, *args, **kwargs)
            if hasattr(response, "context_data"):
                response.context_data[nav] = "active"
            return response

        return wrapper

    return decorator


class NavActive:
    """Mixin to add active menu item to view context."""

    def __init__(self, nav: str) -> None:
        """nav: the name of the navigation section."""
        self.nav = nav

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context[self.nav] = "active"
        return context


class NavPlantActiveContext(NavActive):
    """A mixin for displaying the Plant menu item as selected."""

    def __init__(self) -> None:
        super().__init__("nav_plants")


class NavDescribeActiveContext(NavActive):
    """Class for displaying active navigation in UI for Describe section."""

    def __init__(self) -> None:
        """Initialize the `nav` as 'nav_describe'."""
        super().__init__("nav_describe")


nav_plant_active_context = nav_active("nav_plants")
