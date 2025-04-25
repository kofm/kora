from .base import *

DEBUG = True
STATIC_ROOT = "static/"
SHELL_PLUS = "ipython"


INSTALLED_APPS = [
    "debug_toolbar",
    "django_extensions",
    "django_browser_reload",
    *INSTALLED_APPS,
]

INTERNAL_IPS = ["127.0.0.1", "localhost"]

MIDDLEWARE = [
    "debug_toolbar.middleware.DebugToolbarMiddleware",
    "django_browser_reload.middleware.BrowserReloadMiddleware",
    *MIDDLEWARE,
]

DEBUG_TOOLBAR_ENABLED = True
DEBUG_TOOLBAR_CONFIG = {"SHOW_TOOLBAR_CALLBACK": lambda r: True}
