import functools
from .utils import CONTEXT_KEY


def list_breadcrumb(model):
    def decorator(view_func):
        @functools.wraps(view_func)
        def wrapper(request, *args, **kwargs):
            response = view_func(request, *args, **kwargs)
            if hasattr(response, "context_data"):
                response.context_data[CONTEXT_KEY] = [
                    (
                        model._meta.verbose_name_plural.capitalize(),
                        f"{model._meta.app_label}:{model._meta.verbose_name}_list",
                    ),
                ]
            return response

        return wrapper

    return decorator


def create_breadcrumb(model):
    def decorator(view_func):
        @functools.wraps(view_func)
        def wrapper(request, *args, **kwargs):
            response = view_func(request, *args, **kwargs)
            if hasattr(response, "context_data"):
                response.context_data[CONTEXT_KEY] = [
                    (
                        model._meta.verbose_name_plural.capitalize(),
                        f"{model._meta.app_label}:{model._meta.verbose_name}_list",
                    ),
                ]
            return response

        return wrapper

    return decorator
