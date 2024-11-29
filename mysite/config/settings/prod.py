from .base import *

ALLOWED_HOSTS = [
    '.replit.dev',
    '.localhost',
    '127.0.0.1'
]

DEBUG = False

SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True