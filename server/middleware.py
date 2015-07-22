# -*- coding: utf-8 -*-

from django.conf import settings
from django.http import HttpResponsePermanentRedirect


class SiteMiddleware:

    def process_request(self, request):
        host = request.get_host()
