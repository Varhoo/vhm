#!/usr/bin/python
# -*- coding: utf-8 -*-

# Author: Pavel Studeník
# Email: studenik@varhoo.cz
# Date: 10.2.2010


from datetime import datetime
from time import sleep

from django.core.management.base import BaseCommand, CommandError

from apps.core.models import *
from apps.core.utils import *


class Command(BaseCommand):
    help = ('Get data for render apache\'s sites and director structure')
    requires_model_validation = True
    can_import_settings = True

    def handle(self, *args, **kwargs):
        init(*args, **kwargs)


def init(*args, **kwargs):

    params = ["all", "one"]
    if len(args) != 1 or args[0] not in params:
        print "using: python manage.py update_expire_dns [ all ] \n "
        return False

    if params[0] in args:  # param get all objects
        objects = Domain.objects.all()
        sleep_in_sec = 90

    if params[1] in args:  # param get all objects
        objects = Domain.objects.order_by("last_modify")[:1]
        sleep_in_sec = 1

    for it in objects:
        dns_save_object(it)
        sleep(sleep_in_sec)
