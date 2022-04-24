from .base import *

DEBUG = False
ALLOWED_HOSTS = ['localhost', '0.0.0.0', 'kofm.xyz',  ]
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
