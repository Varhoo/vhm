# -*- coding: utf-8 -*-
# Django Apache IIS

from apps.core import settings
from django.conf import settings as __settings__

SECRET_KEY = getattr(__settings__, "SECRET_KEY", None)
