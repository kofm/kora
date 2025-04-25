"""Project-wide decorators."""

import copy

from django.http.request import HttpRequest, QueryDict
from django.http.response import HttpResponse
from django.utils.functional import wraps
from render_block import render_block_to_string


def is_htmx(request: HttpRequest):
    return request.headers.get("Hx-Request", False)


def htmx_render_blocks(blocks: list):
    def decorator(view):
        @wraps(view)
        def _view(request, *args, **kwargs):
            resp = view(request, *args, **kwargs)

            if not is_htmx(request):
                return resp

            if not hasattr(resp, "render"):
                raise ValueError("@htmx_render_block_from_params should be used with TemplateResponse")

            rendered_blocks = [
                render_block_to_string(
                    resp.template_name,
                    b,
                    context=resp.context_data,
                    request=request,
                )
                for b in blocks
            ]

            resp = HttpResponse(
                content="\n".join(rendered_blocks),
                status=resp.status_code,
                headers=resp.headers,
            )

            return resp

        return _view

    return decorator


def htmx_render_block_from_params():
    def decorator(view):
        @wraps(view)
        def _view(request, *args, **kwargs):
            resp = view(request, *args, **kwargs)

            if not is_htmx(request):
                return resp

            if not hasattr(resp, "render"):
                raise ValueError("@htmx_render_block_from_params should be used with TemplateResponse")

            blocks_to_use = _get_param_from_request(request, "use_block")

            if not blocks_to_use:
                return resp

            rendered_blocks = [
                render_block_to_string(
                    resp.template_name,
                    b,
                    context=resp.context_data,
                    request=request,
                )
                for b in list(blocks_to_use)
            ]
            resp = HttpResponse(
                content="\n".join(rendered_blocks),
                status=resp.status_code,
                headers=resp.headers,
            )

            return resp

        return _view

    return decorator


def _get_param_from_request(request, param):
    """
    Checks GET then POST params for specified param
    """
    if param in request.GET:
        return request.GET.getlist(param)
    elif request.method == "POST" and param in request.POST:
        return request.POST.getlist(param)
    return None


def make_get_request(request: HttpRequest) -> HttpRequest:
    """
    Returns a new GET request based on passed in request.
    """
    new_request = copy.copy(request)
    new_request.POST = QueryDict()
    new_request.method = "GET"
    return new_request


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
nav_describe_active_context = nav_active("nav_describe")
