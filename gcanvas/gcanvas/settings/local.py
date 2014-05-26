#settings/local.py
from .base import *

DEBUG = True
TEMPLATE_DEBUG = DEBUG

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql_psycopg2",
        "NAME": "gcanvas",
        "USER": get_env_variable(""),
        "PASSWORD": "",
        "HOST": "localhost",
        "PORT": "",
    }    
}

INSTALLED_APPS += {"debug_toolbar", }
