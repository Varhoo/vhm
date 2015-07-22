# coding: utf-8

from django.contrib.sites.models import Site
from django.conf import settings
from django.http import HttpResponsePermanentRedirect

import random
from time import time
from math import *

COUNT_ILLUSTRATION = 6


def pages_all(request):
    # admin
    if request.META["PATH_INFO"] in ("admin",):
        return {}

    data = {}

    data["user"] = request.user

    return data
