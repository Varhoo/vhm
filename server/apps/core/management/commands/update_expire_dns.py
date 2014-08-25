#!/usr/bin/python
# -*- coding: utf-8 -*-

#Author: Pavel Studeník
#Email: studenik@varhoo.cz
#Date: 10.2.2010


from django.core.management.base import BaseCommand, CommandError

from apps.apftpmy.models import *
from apps.apftpmy.utils import *

from time import sleep
from datetime import datetime
 
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


    if params[0] in args: #param get all objects
        objects =  Domain.objects.all()
        sleep_in_sec = 90

    if params[1] in args: #param get all objects
        objects =  Domain.objects.order_by("last_modify")[:1]
        sleep_in_sec = 1

    for it in objects:
        old_expr = it.expirate
        new_expr = get_dns_expire(it.name)
        it.last_modify = datetime.now()
        if old_expr != new_expr and new_expr != None:
            it.expirate = new_expr
            print "%s changed  %s -> %s" % (it, old_expr, it.expirate) 
        it.save()
        sleep(sleep_in_sec)
