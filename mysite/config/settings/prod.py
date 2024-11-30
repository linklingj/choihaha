from .base import *

ALLOWED_HOSTS = ['43.201.203.109', 'choihaha.com']

STATIC_URL = BASE_DIR / 'static/'
STATICFILES_DIRS = []

DEBUG = False

# change
SECURE_SSL_REDIRECT = False