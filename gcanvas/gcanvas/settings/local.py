#settings/local.py
from .base import *

#DATABASE_URL=postgres://postgres:<standardbynamepasswordhere>@localhost:5432/gcanvas
#DJANGO_SETTINGS_MODULE=gcanvas.settings.local
#DJANGO_SECRET_KEY=`generate_secret_key.sh`



DEBUG = True
TEMPLATE_DEBUG = DEBUG

#overcomes the not configured bug
DEBUG_TOOLBAR_PATCH_SETTINGS = False

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

#DATABASES = {
#    "default": {
#        "ENGINE": "django.db.backends.postgresql_psycopg2",
#        "NAME": "gcanvas",
#        "USER": get_env_variable(""),
#        "PASSWORD": "",
#        "HOST": "localhost",
#        "PORT": "",
#    }    
#}


INSTALLED_APPS += ("debug_toolbar", )
