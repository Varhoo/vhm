import sys
import os

os.environ['DJANGO_SETTINGS_MODULE'] = 'settings.production'

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)) + '/.')
# This application object is used by any WSGI server configured to use this
# file. This includes Django's development server, if the WSGI_APPLICATION
# setting points here.

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()

