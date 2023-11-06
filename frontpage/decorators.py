"""Project-wide decorators."""


def nav_active(nav):
    """View decorator that adds a key-value pair to the 'context_data' dictionary of a Django view.

    Attributes:
    ------------
    nav : str
        The name of the navigation section that is currently active.
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
    """Class providing support for active navigation in UI. Upon initialization assigns navigation element.

    Attributes:
    ------------
    nav : str
        The name of the navigation section that is currently active.
    """

    def __init__(self, nav) -> None:
        """Initialize NavActive with specified navigation scope.

        Parameters:
        ----------
        nav : str
            The name of the navigation section.
        """
        self.nav = nav

    def get_context_data(self, **kwargs):
        """Retrieve context data and add a marker corresponding to the active navigation section.

        Returns:
        -------
        dict
            The context data including the current active navigation marker.
        """
        context = super().get_context_data(**kwargs)
        context[self.nav] = "active"
        return context
