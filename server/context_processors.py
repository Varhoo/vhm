# coding: utf-8

import random
from math import *
from time import time

from django.conf import settings
from django.contrib.sites.models import Site
from django.http import HttpResponsePermanentRedirect

COUNT_ILLUSTRATION = 6


def pages_all(request):
    # admin
    if request.META["PATH_INFO"] in ("admin",):
        return {}

    data = {}

    data["user"] = request.user

    return data
