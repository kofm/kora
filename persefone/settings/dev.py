import sys

from .base import *

DEBUG = True
STATIC_ROOT = "static/"
SHELL_PLUS = "ipython"
INTERNAL_IPS = ["127.0.0.1", "localhost"]

DEBUG_TOOLBAR_ENABLED = DEBUG and "test" not in sys.argv
DEBUG_TOOLBAR_CONFIG = {"SHOW_TOOLBAR_CALLBACK": lambda r: True}

if DEBUG_TOOLBAR_ENABLED:
    INSTALLED_APPS = [
        "debug_toolbar",
        "django_extensions",
        "django_browser_reload",
        *INSTALLED_APPS,
    ]

    MIDDLEWARE = [
        "debug_toolbar.middleware.DebugToolbarMiddleware",
        "django_browser_reload.middleware.BrowserReloadMiddleware",
        *MIDDLEWARE,
    ]
