def nav_active(key):
    """
    View decorator that adds a key-value pair to the 'context_data' dictionary of a Django view.
    The key name is passed as an argument to the decorator.
    """

    def decorator(view_func):
        def wrapper(request, *args, **kwargs):
            response = view_func(request, *args, **kwargs)
            if hasattr(response, "context_data"):
                response.context_data[key] = "active"
            return response

        return wrapper

    return decorator


class NavActive:
    def __init__(self, nav) -> None:
        self.nav = nav

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context[self.nav] = "active"
        return context
