from django.conf import settings

PATH_PASSWORDS = getattr(settings, "PATH_PASSWORDS", "/etc/apache2/dav_svn.passwd")
PATH_RIGHS = getattr(settings, "PATH_RIGHS", "/etc/apache2/svn_access_control")