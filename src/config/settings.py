import logging
import json
import os
import secrets
from datetime import timedelta
from os.path import join

import sentry_sdk
from corsheaders.defaults import default_headers
from sentry_sdk.integrations.django import DjangoIntegration
from sentry_sdk.integrations.logging import LoggingIntegration

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def get_bool_env(env_var, default=False):
    """
    Retrieve a boolean value from an environment variable.

    This function fetches the value of an environment variable and attempts to
    parse it as a boolean. If the environment variable is not set, the provided
    default value is returned. The function only accepts `True` or `False` as
    valid boolean values.
    """
    val = os.getenv(env_var)
    if val is None:
        return default

    try:
        p = json.loads(val.lower())
        if not isinstance(p, bool):
            raise ValueError("Invalid boolean config: {}".format(val))
        return p
    except (ValueError, json.JSONDecodeError):
        raise ValueError("Invalid boolean config: {}".format(val))


INSTALLED_APPS = (
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "whitenoise.runserver_nostatic",
    "django.contrib.staticfiles",
    "django.contrib.sites",
    # Third party apps
    "rest_framework",  # utilities for rest apis
    "rest_framework.authtoken",  # token authentication
    "django_filters",  # for filtering rest endpoints
    "django_extensions",  # for runserver_plus, shell_plus, show_urls
    # adds Cross-Origin Resource Sharing (CORS) headers to responses
    "corsheaders",
    "django_rest_passwordreset",  # for password reset functionality
    "rest_framework_simplejwt",  # jwt web tokens
    "drf_spectacular",  # for API documentation
    "storages",  # collection of custom storage backends for Django
    # custom apps
    "src.common",
    "src.account",
    "src.recon",
)

# https://docs.djangoproject.com/en/2.0/topics/http/middleware/
MIDDLEWARE = (
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
)

ALLOWED_HOSTS = os.getenv("DJANGO_ALLOWED_HOSTS", "*").split(",")
ROOT_URLCONF = "src.config.urls"
SECRET_KEY = os.getenv("SECRET_KEY")
WSGI_APPLICATION = "src.config.wsgi.application"

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": os.getenv("DATABASE_NAME", ""),
        "USER": os.getenv("DATABASE_USER", ""),
        "PASSWORD": os.getenv("DATABASE_PASSWORD", ""),
        "HOST": os.getenv("DATABASE_HOST", ""),
        "PORT": os.getenv("DATABASE_PORT", ""),
    }
}

# General
APPEND_SLASH = False
TIME_ZONE = "Africa/Nairobi"

LANGUAGE_CODE = "en-us"
# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = False
USE_L10N = True
USE_TZ = True


SITE_ID = 1
APP_NAME = "Recon"

STORAGES = {
    "default": {
        "BACKEND": "django.core.files.storage.FileSystemStorage",
    },
    "staticfiles": {
        "BACKEND": "whitenoise.storage.CompressedStaticFilesStorage",
    },
}

USE_S3 = os.getenv("USE_S3") == "False"

if USE_S3:
    # aws settings
    AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID")
    AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")
    AWS_STORAGE_BUCKET_NAME = os.getenv("AWS_STORAGE_BUCKET_NAME")
    AWS_DEFAULT_ACL = None
    AWS_S3_CUSTOM_DOMAIN = f"{AWS_STORAGE_BUCKET_NAME}.s3.amazonaws.com"
    AWS_S3_OBJECT_PARAMETERS = {"CacheControl": "max-age=86400"}
    # s3 public media settings
    PUBLIC_MEDIA_LOCATION = "media"
    MEDIA_URL = f"https://{AWS_S3_CUSTOM_DOMAIN}/{PUBLIC_MEDIA_LOCATION}/"
    STORAGES["default"] = {
        "BACKEND": "src.common.utils.storage_backends.PublicMediaStorage",
    }
else:
    MEDIA_ROOT = join(os.path.dirname(BASE_DIR), "media")
    MEDIA_URL = "/media/"

STATIC_ROOT = join(os.path.dirname(BASE_DIR), "staticfiles")
STATIC_URL = "/static/"
STATICFILES_DIRS = [join(os.path.dirname(BASE_DIR), "static")]
STATICFILES_FINDERS = (
    "django.contrib.staticfiles.finders.FileSystemFinder",
    "django.contrib.staticfiles.finders.AppDirectoriesFinder",
)

TEMPLATE_DIR = os.path.join(BASE_DIR, "templates")
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
        },
    },
]

# Set DEBUG to False as a default for safety
# https://docs.djangoproject.com/en/dev/ref/settings/#debug

DEBUG = get_bool_env("DJANGO_DEBUG", True)

# Password Validation
# https://docs.djangoproject.com/en/2.0/topics/auth/passwords/#module-django.contrib.auth.password_validation
AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",  # noqa
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",  # noqa
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",  # noqa
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",  # noqa
    },
]

# TODO! to update the below sentry details
sentry_logging = LoggingIntegration(level=logging.INFO, event_level=logging.INFO)
dsn_link = ""
dsn_link_empty = ""
sentry_sdk.init(
    dsn=dsn_link_empty,
    integrations=[DjangoIntegration(), sentry_logging],
    # Set traces_sample_rate to 1.0 to capture 100%
    # of transactions for performance monitoring.
    # We recommend adjusting this value in production,
    traces_sample_rate=1.0,
    # If you wish to associate users to errors (assuming you are using
    # django.contrib.auth) you may enable sending PII data.
    send_default_pii=True,
    # By default the SDK will try to use the SENTRY_RELEASE
    # environment variable, or infer a git commit
    # SHA as release, however you may want to set
    # something more human-readable.
    # release="myapp@1.0.0",
)

# Logging
LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "django.server": {
            "()": "django.utils.log.ServerFormatter",
            "format": "[%(server_time)s] %(message)s",
        },
        "verbose": {
            "format": "%(levelname)s %(asctime)s %(module)s %(process)d %(thread)d %(message)s"  # noqa
        },
        "simple": {"format": "%(levelname)s %(message)s"},
    },
    "filters": {
        "require_debug_true": {
            "()": "django.utils.log.RequireDebugTrue",
        },
    },
    "handlers": {
        "django.server": {
            "level": "INFO",
            "class": "logging.StreamHandler",
            "formatter": "django.server",
        },
        "console": {
            "level": "DEBUG",
            "class": "logging.StreamHandler",
            "formatter": "simple",
        },
        "mail_admins": {
            "level": "ERROR",
            "class": "django.utils.log.AdminEmailHandler",
        },
        "sentry": {
            "level": "ERROR",  # To capture more than ERROR, change to WARNING, INFO, etc. # noqa
            "class": "raven.contrib.django.raven_compat.handlers.SentryHandler",  # noqa
            "tags": {"custom-tag": "x"},
        },
    },
    "loggers": {
        "django": {
            "handlers": ["console"],
            "propagate": True,
        },
        "django.server": {
            "handlers": ["django.server"],
            "level": "INFO",
            "propagate": False,
        },
        "django.request": {
            "handlers": [
                "mail_admins",
                "console",
            ],
            "level": "ERROR",
            "propagate": False,
        },
        "django.db.backends": {
            "handlers": ["console"],
            "level": "INFO",
        },
        "raven": {
            "level": "DEBUG",
            "handlers": ["console"],
            "propagate": False,
        },
        "sentry.errors": {
            "level": "DEBUG",
            "handlers": ["console"],
            "propagate": False,
        },
    },
}

# Custom user app
AUTH_USER_MODEL = "account.User"

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# Django Rest Framework
REST_FRAMEWORK = {
    "DEFAULT_PAGINATION_CLASS": "src.common.paginator.ImprovedPagination",
    "PAGE_SIZE": int(
        os.getenv(
            "DJANGO_PAGINATION_LIMIT",
            40,
        )
    ),
    "EXCEPTION_HANDLER": "src.common.utils.exception_handler.custom_exception_handler",
    "DATETIME_FORMAT": "iso-8601",
    "DATE_FORMAT": "iso-8601",
    "TIME_FORMAT": "iso-8601",
    "DEFAULT_RENDERER_CLASSES": (
        "rest_framework.renderers.JSONRenderer",
        "rest_framework.renderers.BrowsableAPIRenderer",
    ),
    "DEFAULT_PERMISSION_CLASSES": [
        "rest_framework.permissions.IsAuthenticated",
    ],
    "DEFAULT_AUTHENTICATION_CLASSES": (
        "rest_framework_simplejwt.authentication.JWTAuthentication",
    ),
    "DEFAULT_MODEL_SERIALIZER_CLASS": (
        "rest_framework.serializers.HyperlinkedModelSerializer",
        "rest_framework.serializers.ModelSerializer",
    ),
    "DEFAULT_PARSER_CLASSES": (
        "rest_framework.parsers.JSONParser",
        "rest_framework.parsers.FormParser",
        "rest_framework.parsers.MultiPartParser",
        "rest_framework.parsers.FileUploadParser",
    ),
    "DEFAULT_FILTER_BACKENDS": (
        "django_filters.rest_framework.DjangoFilterBackend",
        "rest_framework.filters.OrderingFilter",
        "rest_framework.filters.SearchFilter",
    ),
    "DEFAULT_SCHEMA_CLASS": "drf_spectacular.openapi.AutoSchema",
}

SPECTACULAR_SETTINGS = {
    "TITLE": "Recon API Documentation",
    "DESCRIPTION": "seemless reconciliations",
    "VERSION": "1.0.0",
    "SERVE_INCLUDE_SCHEMA": False,
    "AUTHENTICATION_CLASSES": (
        "rest_framework_simplejwt.authentication.JWTAuthentication",
    ),
    "SWAGGER_UI_SETTINGS": {
        "persistAuthorization": True,
    },
    "SCHEMA_PATH_PREFIX": r"/api/v[0-9]",
    "SORT_OPERATION_PARAMETERS": False,
}

CORS_ALLOWED_ORIGINS = [
    "http://localhost:8080",
]
CORS_ALLOW_HEADERS = default_headers
# email settings
DEFAULT_FROM_EMAIL = os.getenv("DEFAULT_FROM_EMAIL", "admin@recon.co.ke")

# celery settings
CELERY_BROKER_URL = os.getenv("BROKER_URL", "amqp://guest:guest@localhost:5672/")
CELERY_RESULT_BACKEND = "rpc://"
CELERY_TASK_SERIALIZER = "json"
CELERY_TASK_RESULT_EXPIRES = int(os.getenv("CELERY_TASK_RESULT_EXPIRES", 300))
CELERY_TIMEZONE = TIME_ZONE
CELERY_DEFAULT_QUEUE = os.getenv("CELERY_QUEUE", "recon_queue")
CELERY_DEFAULT_EXCHANGE = CELERY_DEFAULT_QUEUE
CELERY_DEFAULT_ROUTING_KEY = CELERY_DEFAULT_QUEUE
SOFT_TIME_DELAY = 60 * 5

SECRET_KEY = os.getenv("SECRET_KEY", secrets.token_urlsafe(32))

SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(seconds=3600),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=7),
    "ROTATE_REFRESH_TOKENS": True,
    "BLACKLIST_AFTER_ROTATION": True,
    "ALGORITHM": "HS256",
    "SIGNING_KEY": SECRET_KEY,
}

# Password `reset strategy
# time in hours about how long the password reset token is active (Default: 24) # noqa
DJANGO_REST_MULTITOKENAUTH_RESET_TOKEN_EXPIRY_TIME = 1
DJANGO_REST_PASSWORDRESET_TOKEN_CONFIG = {
    "CLASS": "django_rest_passwordreset.tokens.RandomNumberTokenGenerator"
}
DJANGO_REST_PASSWORDRESET_TOKEN_CONFIG = {
    "CLASS": "django_rest_passwordreset.tokens.RandomNumberTokenGenerator",
    "OPTIONS": {"min_number": 1500, "max_number": 9999},
}


SITE_CLIENT_DOMAIN = os.getenv("SITE_CLIENT_DOMAIN", "http://localhost:3000")
