from .base import *

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql_psycopg2",
        "NAME": 'gcanvas',
        "USER": 'postgres',
        "PASSWORD": 'postgres',
        "HOST": 'localhost',
        "PORT": 5432,
    }
}


EMAIL_BACKEND = 'django.core.mail.backends.locmem.EmailBackend'

#EMAIL_BACKEND = 'django.core.mail.backends.filebased.EmailBackend'
#EMAIL_FILE_PATH = '/tmp/app-messages' # change this to a proper location

INSTALLED_APPS += (
    "debug_toolbar",
    "django_extensions",
)
