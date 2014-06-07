#settings/local.py
from .base import *
import dj_database_url

#DATABASE_URL=postgres://postgres:<standardbynamepasswordhere>@localhost:5432/gcanvas
#DJANGO_SETTINGS_MODULE=gcanvas.settings.local
#DJANGO_SECRET_KEY=`generate_secret_key.sh`

DATABASES = {
    "default": dj_database_url.config()
}



# Honor the 'X-Forwarded-Proto' header for request.is_secure()
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

# Allow all host headers
ALLOWED_HOSTS = ['*']

DEBUG = True
TEMPLATE_DEBUG = DEBUG

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
