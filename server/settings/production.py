from settings import *

DEBUG = False
TEMPLATE_DEBUG = DEBUG

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',    # Add 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': '',               # Or path to database file if using sqlite3.
        'USER': '',                      # Not used with sqlite3.
        'PASSWORD': '',
        'HOST': 'localhost',                      # Set to empty string for localhost. Not used with sqlite3.
        'PORT': ''                      # Set to empty string for default. Not used with sqlite3.
    }
}

# A sample logging configuration. The only tangible logging
# performed by this configuration is to send an email to
# the site admins on every HTTP 500 error.
# See http://docs.djangoproject.com/en/dev/topics/logging for
# more details on how to customize your logging configuration.

LOGGING = {
    'version': 1,
    'disable_existing_loggers': True,
    'handlers': {
        'mail_admins': {
            'level': 'DEBUG',
            'class': 'django.utils.log.AdminEmailHandler',
        },
        # Log to a text file that can be rotated by logrotate
       'logfile': {
        'level': 'DEBUG',
           'class': 'logging.handlers.WatchedFileHandler',
            'filename': ROOT_PATH + '/../log/error.log'
        }
    },
    'loggers': {
        'django.request': {
            'handlers': ['mail_admins','logfile'],
            'level': 'ERROR',
            'propagate': False,
        },
    }
}


