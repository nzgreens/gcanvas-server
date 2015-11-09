#settings/local.py
from .base import *

#DATABASE_URL=postgres://postgres:<standardbynamepasswordhere>@localhost:5432/gcanvas
#DJANGO_SETTINGS_MODULE=gcanvas.settings.local
#DJANGO_SECRET_KEY=`generate_secret_key.sh`

#NATIONBUILDER_CLIENT_CALLBACK='http://127.0.0.1:8000/nationbuilder/callback'

DEBUG = True
ALLOWED_HOSTS = ['*']
TEMPLATE_DEBUG = DEBUG

#overcomes the not configured bug
DEBUG_TOOLBAR_PATCH_SETTINGS = False

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'


DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql_psycopg2",
        "NAME": 'gcanvas',
        "USER": 'postgres',
        "PASSWORD": 'postgres',
        "HOST": 'database',
        "PORT": 5432,
    }
}


INSTALLED_APPS += (
    "debug_toolbar",
    "django_extensions",
)
