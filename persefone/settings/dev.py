from .base import *

DEBUG = True
STATIC_ROOT = "static/"
SHELL_PLUS = "ipython"

INSTALLED_APPS = [
    "debug_toolbar",
] + INSTALLED_APPS

INTERNAL_IPS = [
    "127.0.0.1",
    "localhost",
]

MIDDLEWARE = [
    "debug_toolbar.middleware.DebugToolbarMiddleware",
] + MIDDLEWARE
# LOGGING = {
#     'version': 1,
#     'disable_existing_loggers': False,
#     'handlers': {
#         'console': {
#             'class': 'logging.StreamHandler',
#         },
#     },
#     'loggers': {
#         'django.db.backends': {
#             'handlers': ['console'],
#             'level': 'DEBUG',
#         },
#     },
# }
