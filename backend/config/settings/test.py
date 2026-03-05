# Test settings for Django with sqlite
from .dev import *

DEBUG = False
SECRET_KEY = 'test-secret-key'
ALLOWED_HOSTS = ['*']

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': ':memory:',
    }
}