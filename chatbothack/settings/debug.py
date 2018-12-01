from .base import *

config_secret_debug = json.loads(open(CONFIG_SECRET_DEBUG_FILE).read())

DEBUG = True
ALLOWED_HOSTS = config_secret_debug['django']['allowed_hosts']

# WSGI application
WSGI_APPLICATION = 'chatbothack.wsgi.debug.application'

ROOT_URLCONF = 'chatbothack.urls.debug'

DATABASES = config_secret_common['django']['database'][0]