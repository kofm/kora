from urllib.parse import urlparse

from django.conf import settings
from django.shortcuts import resolve_url


def htmx_middleware(get_response):
    def middleware(request):
        response = get_response(request)

        if request.headers.get("HX-Request") == "true" and response.status_code == 302:
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
