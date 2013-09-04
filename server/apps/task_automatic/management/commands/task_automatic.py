#!/usr/bin/python
# -*- coding: utf-8 -*-

#Author: Pavel Studeník
#Email: studenik@varhoo.cz
#Date: 28.9.2012

from django.core.management.base import BaseCommand, CommandError
from datetime import datetime
from apps.task_automatic.models import *
from django.core.mail import mail_admins
from django.contrib.auth.models import User
from django.conf import settings
from croniter import croniter

# maybe it was better use value from settings
DEBUG = False

def total_seconds(td):
    # td.total_seconds() only 2.7 version
    return (td.microseconds + (td.seconds + td.days * 24 * 3600) * 10**6) / 10**6.

def debug(str):
    if DEBUG:
        print str

class Command(BaseCommand):
    help = ('Automatization for runnning task')
    requires_model_validation = True
    can_import_settings = True

    def handle(self, *args, **kwargs):
        init(*args, **kwargs)

def init(*args, **kwargs):

    params = ["all", "one"]
    if len(args) != 1 or args[0] not in params:
        print "using: python manage.py taskmatic [all one]\n "
        return False

    try:
        user = User.objects.get(username="taskomatic")
    except User.DoesNotExist:
        user = User(username="taskomatic")
        user.save()

    debug( "DEBUG: task automatic - period" )
    tasks = TaskPeriod.objects.filter(is_enable=True)
 
    for it in tasks:

        citer = croniter(it.cron)
        next_date = citer.get_next(datetime)

        debug( "%s (cron %s ) - last action before %s s." % (it.title, it.cron, it.date_last ) )
        if it.date_start < datetime.now():
            new_task = Task(title="Period: %s" % it.title)
            new_task.common = it.common
            new_task.user = user # create task-atomatic user
            new_task.date_run = next_date
            new_task.save()
            it.date_last=datetime.now()
            it.date_start = next_date
            it.save()
    
    debug( "DEBUG: task automatic" )
    tasks = Task.objects.filter(status=0, date_run__lt=datetime.now())
    for it in tasks:
        debug( "%d - %s" % (it.id, it.title) )
        it.run()
        if  it.status > 2: # 2 = done, 3 = error
            # send email to admins
            subject = "ERROR: mixmotor import: %s - %s" % ( it.title, it.common )
            msg = it.exit_result
            mail_admins(subject, msg)

    # delete old tasks with status DONE, keep only last 100 tasks
    [it.delete() for it in Task.objects.filter(status=2).order_by("-date_run")[100:]]
