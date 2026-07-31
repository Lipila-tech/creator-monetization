from .base import *

# False if not in os.environ because of casting above
DEBUG = env.bool('DEBUG', default=False)

ALLOWED_HOSTS = env('ALLOWED_HOSTS', default='localhost,127.0.0.1').split(',')

# CORS Configuration for multi-frontend support
CORS_ALLOWED_ORIGINS = env(
    'CORS_ALLOWED_ORIGINS', default='http://localhost:5173,http://127.0.0.1:5173').split(',')

CORS_ALLOW_CREDENTIALS = True

CORS_ALLOW_HEADERS = (
    *default_headers,
    "x-api-key",  # Allow the custom header
)

CSRF_TRUSTED_ORIGINS = env('CSRF_TRUSTED_ORIGINS',
                           default='http://localhost:5173').split(',')

# Configure Gmail Email settings
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'

# Configure Logging to capture errors and important info in production
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'level': 'INFO',  # Use 'DEBUG' for more verbosity, 'INFO' is standard for production
            'class': 'logging.StreamHandler',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['console'],
            'level': 'INFO',  # Ensure this is low enough to catch errors
            'propagate': True,
        },
    },
    'root': {
        'handlers': ['console'],
        'level': 'INFO',
    },
}


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

