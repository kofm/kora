import os
from pathlib import Path

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

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
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
USE_I18N = True
USE_L10N = True
USE_TZ = False
FORMAT_MODULE_PATH = [
    "formats",
]  # <project>/formats, because this has global effect

STATIC_URL = "static/"

CRISPY_ALLOWED_TEMPLATE_PACKS = "bootstrap5"
CRISPY_TEMPLATE_PACK = "bootstrap5"
DJANGO_TABLES2_TEMPLATE = "django_tables2/bootstrap5.html"

LOGIN_REDIRECT_URL = "/"
LOGOUT_REDIRECT_URL = "/"
