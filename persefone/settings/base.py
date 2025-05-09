import os
from pathlib import Path

from django.contrib import messages

BASE_DIR = Path(__file__).resolve().parent.parent
TEMPLATE_DIR = Path(BASE_DIR) / "templates"

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django.contrib.postgres",
    "django_tables2",
    "django_filters",
    "drf_redesign",
    "rest_framework",
    "crispy_forms",
    "crispy_bootstrap5",
    "django_countries",
    "widget_tweaks",
    "easyaudit",
    "register.apps.RegisterConfig",
    "describe.apps.DescribeConfig",
    "frontpage.apps.FrontpageConfig",
    "parameters.apps.ParametersConfig",
    "spaces.apps.SpacesConfig",
    "calculator.apps.CalculatorConfig",
    "collect.apps.CollectConfig",
    "django_sortable_htmx",
    "breadcrumbs",
    "render_block",
]

PUBLIC = os.getenv("PUBLIC", "").lower() in ("1", "true", "yes")

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    *([] if PUBLIC else ["django.contrib.auth.middleware.LoginRequiredMiddleware"]),
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "frontpage.middleware.htmx_login_redirect_middleware",
    "frontpage.middleware.htmx_message_middleware",
    "easyaudit.middleware.easyaudit.EasyAuditMiddleware",
]
ROOT_URLCONF = "persefone.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [TEMPLATE_DIR],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
            "builtins": [],
        },
    },
]

WSGI_APPLICATION = "persefone.wsgi.application"

# Password validation
AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
        "OPTIONS": {
            "min_length": 9,
        },
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]

# Database configuration. These defaults make sense for use via
# `kora-docker` (https://github.com/kofm/kora-docker). Host, port, and
# password have to be set in the running environment.
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": "postgres",
        "USER": "postgres",
        "PASSWORD": os.getenv("POSTGRES_PASSWORD", "postgres"),
        "HOST": os.getenv("DB_HOST", "localhost"),
        "PORT": os.getenv("DB_PORT", "5432"),
    },
}

DEFAULT_AUTO_FIELD = "django.db.models.AutoField"

hosts = os.getenv("ALLOWED_HOSTS", "")
ALLOWED_HOSTS = hosts.split() if hosts else []

origins = os.getenv("CSRF_TRUSTED_ORIGINS", "")
CSRF_TRUSTED_ORIGINS = origins.split() if origins else []

# Internationalization
LANGUAGE_CODE = "en-GB"
TIME_ZONE = "UTC"
USE_I18N = False
USE_TZ = True
FORMAT_MODULE_PATH = ("formats",)

STATIC_URL = "static/"

CRISPY_ALLOWED_TEMPLATE_PACKS = "bootstrap5"
CRISPY_TEMPLATE_PACK = "bootstrap5"
DJANGO_TABLES2_TEMPLATE = "django_tables2/bootstrap5-responsive.html"
DJANGO_TABLES2_PAGE_RANGE = 10

REST_FRAMEWORK = {
    "DEFAULT_PAGINATION_CLASS": "restapi.pagination.OptionalPagination",
    "PAGE_SIZE": 10,
    "DEFAULT_PERMISSION_CLASSES": [
        "rest_framework.permissions.IsAuthenticated",
    ],
}

LOGIN_REDIRECT_URL = "/"
LOGOUT_REDIRECT_URL = "/"
MESSAGE_TAGS = {
    messages.DEBUG: "bg-light",
    messages.INFO: "text-white bg-primary",
    messages.SUCCESS: "text-white bg-success",
    messages.WARNING: "text-dark bg-warning",
    messages.ERROR: "text-white bg-danger",
}

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "handlers": {
        "file": {
            "class": "logging.FileHandler",
            "filename": "kora.log",
            "level": "DEBUG" if os.getenv("DEV", False) else "WARNING",
            "formatter": "verbose",
        },
    },
    "loggers": {
        "": {
            "level": "DEBUG",
            "handlers": ["file"],
        },
    },
    "formatters": {
        "verbose": {
            "format": "%(asctime)s %(levelname)s [%(name)s] %(message)s",
        },
        "simple": {
            "format": "{levelname} {message}",
            "style": "{",
        },
    },
}


# Defines whether to log model related events, such as when an
# object is created, updated, or deleted. Defaults to True.
DJANGO_EASY_AUDIT_WATCH_MODEL_EVENTS = True

# Defines whether to log user authentication events, such as logins,
# logouts and failed logins. Defaults to True.
DJANGO_EASY_AUDIT_WATCH_AUTH_EVENTS = False

# Defines whether to log URL requests made to the project. Defaults to
# True
DJANGO_EASY_AUDIT_WATCH_REQUEST_EVENTS = False

DJANGO_EASY_AUDIT_UNREGISTERED_CLASSES_EXTRA = ["auth.group"]
