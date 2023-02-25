from .base import *

DEBUG = True
ALLOWED_HOSTS = ['localhost', '0.0.0.0', 'web'  ]
CSRF_TRUSTED_ORIGINS = ['http://localhost:8001/*', 'http://web']

# Database
# https://docs.djangoproject.com/en/3.1/ref/settings/#databases
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": "postgres",
        "USER": "postgres",
        "PASSWORD": "postgres",
        "HOST": "db",
        "PORT": 5432,
    },
}

STATIC_ROOT = "/var/www/static/"
# DEFAULT_EXCEPTION_REPORTER = "exceptionite.django.ExceptioniteReporter"
SHELL_PLUS = "ipython"

INTERNAL_IPS = [
    "127.0.0.1",
]
