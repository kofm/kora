import os
import sys
from pathlib import Path

from django.contrib import messages

from frontpage.utils.env_utils import getenv_bool, getenv_list

# Environment-fetched settings

SECRET_KEY = os.getenv("SECRET_KEY")
DEV = getenv_bool("DEV")
ALLOWED_HOSTS = getenv_list("ALLOWED_HOSTS")
CSRF_TRUSTED_ORIGINS = getenv_list("CSRF_TRUSTED_ORIGINS")

PUBLIC = getenv_bool("PUBLIC")
USE_HTTPS = getenv_bool("USE_HTTPS", False)
AUTHLOG_ENABLED = getenv_bool("AUTHLOG_ENABLED", False)

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
    "django.forms",
    "django_tables2",
    "django_filters",
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
    "restapi",
    "django_sortable_htmx",
    "breadcrumbs",
    "render_block",
    "drf_spectacular",
]

# Conditionally add authentication logging
if AUTHLOG_ENABLED:
    INSTALLED_APPS.append("authlog")

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
        "NAME": os.getenv("DB_NAME", "postgres"),
        "USER": os.getenv("DB_USER", "postgres"),
        "PASSWORD": os.environ["DB_PASSWORD"],
        "HOST": os.getenv("DB_HOST", "localhost"),
        "PORT": os.getenv("DB_PORT", "5432"),
    },
}

DEFAULT_AUTO_FIELD = "django.db.models.AutoField"

# Internationalization
LANGUAGE_CODE = "en-GB"
TIME_ZONE = "UTC"
USE_I18N = False
USE_TZ = True
FORMAT_MODULE_PATH = ("formats",)

# Static Files
STATIC_URL = "static/"

# crispy_forms
CRISPY_ALLOWED_TEMPLATE_PACKS = "bootstrap5"
CRISPY_TEMPLATE_PACK = "bootstrap5"

# django_tables2
DJANGO_TABLES2_TEMPLATE = "django_tables2/bootstrap5-responsive.html"
DJANGO_TABLES2_PAGE_RANGE = 10

# rest_framework
REST_FRAMEWORK = {
    "DEFAULT_PAGINATION_CLASS": "rest_framework.pagination.LimitOffsetPagination",
    "PAGE_SIZE": 100,
    "DEFAULT_RENDERER_CLASSES": [
        "rest_framework.renderers.JSONRenderer",
        "restapi.renderers.NoWriteFormsBrowsableAPIRenderer",
    ],
    "DEFAULT_FILTER_BACKENDS": [
        "restapi.filters.NoBrowsableAPIFilterBackend",
    ],
    "DEFAULT_PERMISSION_CLASSES": [
        "rest_framework.permissions.IsAuthenticated",
    ],
    "TEST_REQUEST_DEFAULT_FORMAT": "json",
    "DEFAULT_SCHEMA_CLASS": "drf_spectacular.openapi.AutoSchema",
}

SPECTACULAR_SETTINGS = {
    "TITLE": "Kora API",
    "DESCRIPTION": "API for managing plant genetic resources data.",
    "COMPONENT_SPLIT_REQUEST": True,
}

# Authentication
LOGIN_REDIRECT_URL = "/"
LOGOUT_REDIRECT_URL = "/"

# Messages
MESSAGE_TAGS = {
    messages.DEBUG: "bg-light",
    messages.INFO: "text-white bg-primary",
    messages.SUCCESS: "text-white bg-success",
    messages.WARNING: "text-dark bg-warning",
    messages.ERROR: "text-white bg-danger",
}

# Logging
LOGGING: dict = {
    "version": 1,
    "disable_existing_loggers": False,
    "handlers": {},
    "loggers": {},
    "formatters": {},
}

if AUTHLOG_ENABLED:
    from authlog.logging import AUTHLOG_FORMATTER, AUTHLOG_HANDLER, AUTHLOG_LOGGER

    LOGGING["handlers"].update(AUTHLOG_HANDLER)
    LOGGING["loggers"].update(AUTHLOG_LOGGER)
    LOGGING["formatters"].update(AUTHLOG_FORMATTER)

# easy_audit
# Defines whether to log model related events, such as when an object
# is created, updated, or deleted. Defaults to True.
DJANGO_EASY_AUDIT_WATCH_MODEL_EVENTS = getenv_bool("DJANGO_EASY_AUDIT_WATCH_MODEL_EVENTS", True)

# Defines whether to log user authentication events, such as logins,
# logouts and failed logins. Defaults to False
DJANGO_EASY_AUDIT_WATCH_AUTH_EVENTS = getenv_bool("DJANGO_EASY_AUDIT_WATCH_AUTH_EVENTS", False)

# Defines whether to log URL requests made to the project. Defaults to
# False
DJANGO_EASY_AUDIT_WATCH_REQUEST_EVENTS = getenv_bool("DJANGO_EASY_AUDIT_WATCH_REQUEST_EVENTS", False)

DJANGO_EASY_AUDIT_UNREGISTERED_CLASSES_EXTRA = getenv_list(
    "DJANGO_EASY_AUDIT_UNREGISTERED_CLASSES_EXTRA",
    ["auth.group"],
)

DJANGO_EASY_AUDIT_UNREGISTERED_CLASSES_EXTRA.append("describe.StateGroup")
DJANGO_EASY_AUDIT_UNREGISTERED_CLASSES_EXTRA.append("collect.StoragePosition")

# Conditional settings

if DEV:
    DEBUG = True
    INTERNAL_IPS = ["127.0.0.1", "localhost"]

    SHELL_PLUS = "ipython"

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

else:
    DEBUG = False
    STATIC_ROOT = "/var/www/static/"

    DEBUG_TOOLBAR_ENABLED = False

    SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https") if USE_HTTPS else None
    SESSION_COOKIE_SECURE = USE_HTTPS
    CSRF_COOKIE_SECURE = USE_HTTPS
