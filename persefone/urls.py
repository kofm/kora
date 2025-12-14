"""kora URL Configuration"""

from django.contrib import admin
from django.urls import include, path

from frontpage.views import KoraLoginView
from persefone import settings

urlpatterns = [
    path("django-admin/", admin.site.urls),
    path("accounts/login/", KoraLoginView.as_view(), name="login"),
    path("accounts/", include("django.contrib.auth.urls")),
    path("", include("frontpage.urls")),
    path("", include("register.urls")),
    path("descriptions/", include("describe.urls")),
    path("parameters/", include("parameters.urls")),
    path("api/", include("restapi.urls")),
    path("spaces/", include("spaces.urls")),
    path("collect/", include("collect.urls")),
    path("plan/", include("calculator.urls")),
]

if settings.DEBUG and settings.DEBUG_TOOLBAR_ENABLED:
    from debug_toolbar.toolbar import debug_toolbar_urls

    urlpatterns = [path("__reload__/", include("django_browser_reload.urls")), *urlpatterns]
    urlpatterns = urlpatterns + debug_toolbar_urls()
