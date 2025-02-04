# Django Admin Bulk i/o Constants
from dotenv import dotenv_values

config = dotenv_values(".env")

DJANGO_DATABASE_URL = config["DATABASE_URL"]


class Settings:
    """Settings Constants"""

    SECRET_KEY = config["SECRET_KEY"]
    DATABASE_URL = config["DATABASE_URL"]
    ROOT_URLCONF = "django_admin_bulk_io.urls"
    TEMPLATES = "templates"
    WSGI_APPLICATION = "django_admin_bulk_io.wsgi.application"
    STATIC_URL = "/static/"
    STATIC_FILES_DIRS = "templates/static/"
    STATIC_ROOT = "assets/"
    MEDIA_URL = "/media/"
    MEDIA_ROOT = "media"
    LANGUAGE_CODE = "en-us"
    TIME_ZONE = "Asia/Kolkata"
    USE_I18N = True
    USE_TZ = True


class EmailConfig:
    """Email Constants"""

    EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
    EMAIL_HOST = "smtp.gmail.com"
    PORT_587 = 587
    PORT_465 = 465
    EMAIL_HOST_USER = config["EMAIL_HOST_USER"]
    EMAIL_HOST_PASSWORD = config["EMAIL_HOST_PASSWORD"]


class CeleryConfig:
    """Celery Config"""

    CELERY_BROKER_URL = "redis://localhost:6379/0"
