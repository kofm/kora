from django.conf import settings
from django.contrib import admin
from django.urls import include, path

from persefone.views import readiness

urlpatterns = [
    path("ready/", readiness, name="readiness"),
    path("django-admin/", admin.site.urls),
    path("accounts/", include("django.contrib.auth.urls")),
    path("", include("frontpage.urls")),
    path("", include("register.urls")),
    path("describe/", include("describe.urls")),
    path("parameters/", include("parameters.urls")),
    path("api/", include("restapi.urls")),
    path("spaces/", include("spaces.urls")),
    path("collect/", include("collect.urls")),
    path("plan/", include("calculator.urls")),
]


if settings.DEBUG_TOOLBAR_ENABLED:
    from debug_toolbar.toolbar import debug_toolbar_urls

    urlpatterns = [
        path("__reload__/", include("django_browser_reload.urls")),
        *urlpatterns,
        *debug_toolbar_urls(),
    ]
