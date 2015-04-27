# coding: utf-8
# Django settings for apacheiis project.

DEBUG = True
TEMPLATE_DEBUG = DEBUG
#EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend' 

import os
ROOT_PATH = os.path.abspath("%s/../" % os.path.dirname(os.path.realpath(__file__)))

ADMINS = (
     ('Pavel Studenik', 'studenik@varhoo.cz'),
)

MANAGERS = ADMINS

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',	 # Add 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': '%s/data.db' % ROOT_PATH,               # Or path to database file if using sqlite3.
        'USER': '',                      # Not used with sqlite3.
        'PASSWORD': '', 
        'HOST': '',                      # Set to empty string for localhost. Not used with sqlite3.
        'PORT': ''                      # Set to empty string for default. Not used with sqlite3.
    }
}

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# On Unix systems, a value of None will cause Django to use the same
# timezone as the operating system.
# If running in a Windows environment this must be set to the same as your
# system time zone.
TIME_ZONE = 'Europe/Prague'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'cs-CZ'

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# If you set this to False, Django will not format dates, numbers and
# calendars according to the current locale
USE_L10N = True

# Absolute filesystem path to the directory that will hold user-uploaded files.
# Example: "/home/media/media.lawrence.com/media/"
MEDIA_ROOT = (
    "%s/%s/" % (ROOT_PATH, 'media')
)


# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash.
# Examples: "http://media.lawrence.com/media/", "http://example.com/media/"
MEDIA_URL = '/media/'

# Absolute path to the directory static files should be collected to.
# Don't put anything in this directory yourself; store your static files
# in apps' "static/" subdirectories and in STATICFILES_DIRS.
# Example: "/home/media/media.lawrence.com/static/"
STATIC_ROOT = "%s/%s/" % (ROOT_PATH, 'static')


# URL prefix for static files.
# Example: "http://media.lawrence.com/static/"
STATIC_URL = '/static/'

ADMIN_MEDIA_PATH =  ROOT_PATH + '/static/grappelli/'

# Make this unique, and don't share it with anybody.
SECRET_KEY = 'h*fq2k11@o$byy@j^633lszuzqijzc!(y^!0c=14z2@qhkif23'

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
#     'django.template.loaders.eggs.Loader',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'middleware.SiteMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
)

ROOT_URLCONF = 'urls'

TEMPLATE_DIRS = (
    # Put strings here, like "/home/html/django_templates" or "C:/www/django/templates".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
    ROOT_PATH + "/templates/",
)

# List of finder classes that know how to find static files in
# various locations.
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
#    'django.contrib.staticfiles.finders.DefaultStorageFinder',
)


TEMPLATE_CONTEXT_PROCESSORS = (
    "django.contrib.auth.context_processors.auth",
    "django.core.context_processors.debug",
    "django.core.context_processors.i18n",
    "django.core.context_processors.media",
    "django.core.context_processors.static",
    "django.contrib.messages.context_processors.messages",
    "context_processors.pages_all"
)

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # Uncomment the next line to enable the admin:
    'grappelli',
    'filebrowser',
    'django.contrib.admin',
    # Uncomment the next line to enable admin documentation:
    'django.contrib.admindocs',
    'apps.core',
    'apps.ticket',
    'apps.svn_dav',
    'apps.auth',
    'apps.consumer',
    'apps.xmlrpc',
    'apps.task_automatic',
    "apps.monitoring",
    "apps.client",
    "south",
)

AUTH_PROFILE_MODULE = 'apps.auth.models.UserProfil'

APACHE_GROUP = "webuser"

# nastavení administrace
GRAPPELLI_ADMIN_HEADLINE =  'Varhoo Administrace'
GRAPPELLI_ADMIN_TITLE = 'Varhoo Administrace'

FILEBROWSER_MEDIA_ROOT = "%s/media/" % ROOT_PATH
FILEBROWSER_DIRECTORY = ""
FILEBROWSER_MEDIA_URL = "/media/"

TINYMCE_JS_URL = "/media/grappelli/tinymce/jscripts/tiny_mce/tiny_mce.js"
TINYMCE_JS_ROOT =  MEDIA_ROOT + "grappelli/tinymce/jscripts/tiny_mce/"