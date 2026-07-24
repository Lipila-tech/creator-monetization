# Test settings for Django with sqlite
from .base import *

DEBUG = False
SECRET_KEY = 'test-secret-key'
ALLOWED_HOSTS = ['*']

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'



DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': ':memory:',
    }
}
