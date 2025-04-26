from urllib.parse import urlparse

from django.conf import settings
from django.contrib.messages import get_messages
from django.shortcuts import resolve_url
from django.template.loader import render_to_string

from frontpage.views_decorators import is_htmx


def htmx_login_redirect_middleware(get_response):
    def middleware(request):
        response = get_response(request)

        if is_htmx(request) and response.status_code == 302:
            redirect_location = response.get("Location", "")
            login_url = resolve_url(settings.LOGIN_URL)
            parsed_redirect = urlparse(redirect_location)

            # Trigger only if the redirect is to the login page
            if parsed_redirect.path == login_url:
                referer = urlparse(request.headers.get("Referer", ""))
                querystring = f"?next={referer.path}" if referer.path else ""

                response.status_code = 204
                response.headers["HX-Redirect"] = f"{login_url}{querystring}"

        return response

    return middleware


def htmx_message_middleware(get_response):
    def middleware(request):
        response = get_response(request)
        messages = get_messages(request)

        if not messages:
            return response

        if is_htmx(request) and not 300 <= response.status_code < 400 and "HX-Redirect" not in response.headers:
            response.write(
                render_to_string(
                    template_name="frontpage/partials/toasts.html",
                    context={"messages": messages},
                    request=request,
                )
            )

        return response

    return middleware
