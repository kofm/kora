from .base import *

DEBUG = True
CSRF_TRUSTED_ORIGINS = [
    "http://localhost:8001/*",
]
STATIC_ROOT = "static/"
SHELL_PLUS = "ipython"
INTERNAL_IPS = [
    "127.0.0.1",
]
