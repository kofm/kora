from django.contrib.auth.decorators import login_not_required
from django.db import connection
from django.http import HttpResponse
from django.views.decorators.http import require_GET


@login_not_required
@require_GET
def readiness(request):
    try:
        connection.ensure_connection()
    except Exception:
        return HttpResponse("database unavailable\n", status=503, content_type="text/plain")

    return HttpResponse("ready\n", content_type="text/plain")
