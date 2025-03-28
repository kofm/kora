from .base import *

DEBUG = True
STATIC_ROOT = "static/"
SHELL_PLUS = "ipython"

INSTALLED_APPS = [
    "debug_toolbar",
    "django_extensions",
] + INSTALLED_APPS

INTERNAL_IPS = [
    "127.0.0.1",
    "localhost",
]

MIDDLEWARE = [
    "debug_toolbar.middleware.DebugToolbarMiddleware",
] + MIDDLEWARE

DEBUG_TOOLBAR_CONFIG = {
    "SHOW_TOOLBAR_CALLBACK": lambda r: True,  # disables it
    # '...
}
