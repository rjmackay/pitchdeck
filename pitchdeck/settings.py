"""
For the full list of settings and their values,
see https://docs.djangoproject.com/en/3.0/ref/settings/
"""
import os
from typing import Optional

from configurations import Configuration
from configurations import values
import sentry_sdk
from sentry_sdk.integrations.django import DjangoIntegration
from sentry_sdk.integrations.redis import RedisIntegration


class Common(Configuration):
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

    MEDIA_ROOT = os.path.join(BASE_DIR, "media")

    SECRET_KEY = values.SecretValue()
    DEBUG = values.BooleanValue(False)

    ALLOWED_HOSTS = ["*"]

    INTERNAL_IPS = ["127.0.0.1"]

    # Application definition
    INSTALLED_APPS = [
        "whitenoise.runserver_nostatic",
        "django.contrib.admin",
        "django.contrib.auth",
        "django.contrib.contenttypes",
        "django.contrib.sessions",
        "django.contrib.messages",
        "django.contrib.staticfiles",
        "django_extensions",
        "django_rq",
        "material",
        "apps.core",
    ]

    MIDDLEWARE = [
        "django.middleware.security.SecurityMiddleware",
        "django.contrib.sessions.middleware.SessionMiddleware",
        "django.middleware.common.CommonMiddleware",
        "django.middleware.csrf.CsrfViewMiddleware",
        "django.contrib.auth.middleware.AuthenticationMiddleware",
        "django.contrib.messages.middleware.MessageMiddleware",
        "django.middleware.clickjacking.XFrameOptionsMiddleware",
        "whitenoise.middleware.WhiteNoiseMiddleware",
    ]

    ROOT_URLCONF = "pitchdeck.urls"

    TEMPLATES = [
        {
            "BACKEND": "django.template.backends.django.DjangoTemplates",
            "DIRS": [],
            "APP_DIRS": True,
            "OPTIONS": {
                "context_processors": [
                    "django.template.context_processors.debug",
                    "django.template.context_processors.request",
                    "django.contrib.auth.context_processors.auth",
                    "django.contrib.messages.context_processors.messages",
                ]
            },
        }
    ]

    WSGI_APPLICATION = "pitchdeck.wsgi.application"

    # Password validation
    # https://docs.djangoproject.com/en/3.0/ref/settings/#auth-password-validators
    AUTH_PASSWORD_VALIDATORS = [
        {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
        {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
        {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
        {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
    ]

    # Internationalization
    # https://docs.djangoproject.com/en/3.0/topics/i18n/
    LANGUAGE_CODE = "en-us"

    TIME_ZONE = "UTC"

    USE_I18N = True

    USE_L10N = True

    USE_TZ = True

    # Static files (CSS, JavaScript, Images)
    # See http://whitenoise.evans.io/en/stable/
    STATIC_URL = "/static/"

    MEDIA_URL = "/media/"

    # SESSION_COOKIE_SECURE = False
    # SECURE_BROWSER_XSS_FILTER = False
    # SECURE_CONTENT_TYPE_NOSNIFF = False
    # SECURE_HSTS_INCLUDE_SUBDOMAINS = False
    # SECURE_HSTS_SECONDS = 86400
    # SECURE_REDIRECT_EXEMPT = []
    # SECURE_SSL_HOST = None
    # SECURE_SSL_REDIRECT = False
    # SECURE_PROXY_SSL_HEADER = (
    #     ('HTTP_X_FORWARDED_PROTO', 'https'),
    # )

    # Sentry
    SENTRY_DSN: Optional[str] = values.URLValue(environ_prefix=None, default=None)
    if SENTRY_DSN:
        sentry_sdk.init(dsn=SENTRY_DSN, integrations=[DjangoIntegration(), RedisIntegration()])

    # Database
    DATABASES = values.DatabaseURLValue()

    # Cache
    CACHES = values.CacheURLValue(default="locmem://")

    # Queue
    REDIS_URL = values.Value(environ_prefix=None)
    RQ_ASYNC = True

    @property
    def RQ_QUEUES(self):
        return {
            "default": {
                "URL": self.REDIS_URL,
                "DEFAULT_TIMEOUT": 360,
                "ASYNC": self.RQ_ASYNC,
            },
        }


class Dev(Common):
    DEBUG = True


class Test(Common):
    RQ_ASYNC = False


class Prod(Common):
    # Media storage
    DEFAULT_FILE_STORAGE = "storages.backends.s3boto3.S3Boto3Storage"

    # AWS
    AWS_ACCESS_KEY_ID = values.Value(environ_prefix="", environ_name="BUCKETEER_AWS_ACCESS_KEY_ID")
    AWS_SECRET_ACCESS_KEY = values.Value(environ_prefix="", environ_name="BUCKETEER_AWS_SECRET_ACCESS_KEY")
    AWS_STORAGE_BUCKET_NAME = values.Value(environ_prefix="", environ_name="BUCKETEER_BUCKET_NAME")

    AWS_DEFAULT_ACL = None
    AWS_S3_OBJECT_PARAMETERS = {"CacheControl": "max-age=86400"}
    AWS_QUERYSTRING_AUTH = values.BooleanValue(False, environ_prefix="")
    AWS_LOCATION = "pitchdeck/"
