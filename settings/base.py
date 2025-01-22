from os.path import join
from pathlib import Path

from dj_database_url import config
from django.utils.timezone import timedelta  # noqa

from utils.constants import Settings, EmailConfig, CeleryConfig

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent
APPEND_SLASH = True
ROOT_URLCONF = Settings.ROOT_URLCONF

admins = (("Mohit Prajapat", """mohit.prajapat@trootech.com"""),)


# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = Settings.SECRET_KEY

# Installed Apps
DJANGO_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
]

# Project Apps
PROJECT_APPS = ["bulk_io_test.apps.BulkIoTestConfig", "django_admin_bulk_io"]

# Third Party Apps
THIRD_PARTY_APPS = ["django_extensions"]


INSTALLED_APPS = THIRD_PARTY_APPS + PROJECT_APPS + DJANGO_APPS


# Middlewares
MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

# Root Urls
ROOT_URLCONF = Settings.ROOT_URLCONF

# Templates + Context Processors
TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        # "DIRS": [join(BASE_DIR, Settings.TEMPLATES)],
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

# WSGI - Web Server Gateway Interface Server
WSGI_APPLICATION = Settings.WSGI_APPLICATION


# Database
# https://docs.djangoproject.com/en/5.1/ref/settings/#databases
DATABASES = {"default": config(default=Settings.DATABASE_URL)}

# Password validation
# https://docs.djangoproject.com/en/5.1/ref/settings/#auth-password-validators
AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]


# Internationalization
# https://docs.djangoproject.com/en/5.1/topics/i18n/
LANGUAGE_CODE = Settings.LANGUAGE_CODE

TIME_ZONE = Settings.TIME_ZONE

USE_I18N = Settings.USE_I18N

USE_TZ = Settings.USE_TZ


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.1/howto/static-files/
STATIC_URL = Settings.STATIC_URL
STATICFILES_DIRS = [join(BASE_DIR, Settings.STATIC_FILES_DIRS)]
STATIC_ROOT = join(BASE_DIR, Settings.STATIC_ROOT)

# Media files (Models File)
MEDIA_URL = Settings.MEDIA_URL
MEDIA_ROOT = join(BASE_DIR, Settings.MEDIA_ROOT)


# Default primary key field type
# https://docs.djangoproject.com/en/5.1/ref/settings/#default-auto-field
# -------------------------------------------------
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"


# Email Configuration
EMAIL_BACKEND = EmailConfig.EMAIL_BACKEND
EMAIL_HOST = EmailConfig.EMAIL_HOST
EMAIL_USE_SSL = True  # use port 465
EMAIL_USE_TLS = False  # use port 587
EMAIL_PORT = EmailConfig.PORT_465 if EMAIL_USE_SSL else EmailConfig.PORT_587
EMAIL_HOST_USER = EmailConfig.EMAIL_HOST_USER
EMAIL_HOST_PASSWORD = EmailConfig.EMAIL_HOST_PASSWORD

# Celery Configuration
CELERY_BROKER_URL = CeleryConfig.CELERY_BROKER_URL
CELERY_TIMEZONE = Settings.TIME_ZONE
CELERY_RESULT_BACKEND = "redis"
CELERY_ACCEPT_CONTENT = ["application/json"]
CELERY_TASK_SERIALIZER = "json"
CELERY_RESULT_EXTENDED = True

# Logging Configuration
LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "verbose": {
            "format": "{levelname} {module} {message}",
            "style": "{",
        },
    },
    "handlers": {
        "file": {
            "level": "DEBUG",
            "class": "logging.FileHandler",
            "filename": "debug.log",
            "formatter": "verbose",
        },
        "console": {
            "class": "logging.StreamHandler",
        },
    },
    "root": {
        "handlers": ["console", "file"],
        "level": "INFO",
    },
}
