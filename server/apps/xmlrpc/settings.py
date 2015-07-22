# -*- coding: utf-8 -*-
# Django Apache IIS

from django.conf import settings as __settings__

from apps.core import settings

SECRET_KEY = getattr(__settings__, "SECRET_KEY", None)
