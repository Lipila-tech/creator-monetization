from .base import *


# False if not in os.environ because of casting above
DEBUG = True

# CORS Configuration for multi-frontend support

CORS_ALLOW_ALL_ORIGINS = True # for development only
CORS_ALLOW_CREDENTIALS = True

CORS_ALLOW_HEADERS = (
    *default_headers,
    "x-api-key",  # Allow the custom header
)
CSRF_TRUSTED_ORIGINS = env('CSRF_TRUSTED_ORIGINS', default='http://localhost:5173').split(',')

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

# Parse database connection url strings
# like psql://user:pass@127.0.0.1:8458/db
DATABASES = {
    # read os.environ['DATABASE_URL'] and raises
    # ImproperlyConfigured exception if not found
    #
    # The db() method is an alias for db_url().
    'default': env.db(),

    # read os.environ['SQLITE_URL']
    'extra': env.db_url(
        'SQLITE_URL',
        default='sqlite:///db.sqlite3'
    )
}
