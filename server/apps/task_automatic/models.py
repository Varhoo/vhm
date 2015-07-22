# -*- coding: utf-8 -*-
# Author: Pavel Studeník
# Email: studenik@varhoo.cz
# Date: 10.2.2010

import random
import traceback
from datetime import *

from django.contrib.auth.models import User
from django.db import models
from django.template.defaultfilters import filesizeformat
from django.utils.translation import ugettext_lazy as _

import settings
from enums import *


class Task(models.Model):
    user = models.ForeignKey(User)
    title = models.CharField(max_length=64)
    common = models.CharField(max_length=128)
    status = models.IntegerField(default=0, choices=STATUS_ENUM)
    exit_result = models.TextField(_('Result log'), blank=True)
    date_create = models.DateTimeField(
        _('Date of create'), default=datetime.now())
    date_run = models.DateTimeField(_('Date of pick up'))
    time_long = models.FloatField(default=0.0)  # better set to NULL

    def __unicode__(self):
        return self.title

    def get_time_long(self):
        t = timedelta(seconds=self.time_long)
        return str(t)

    def run(self):
        t1 = datetime.now()
        self.status = 1  # set status "in progress"
        self.save()

        # --- RUN --- #
        if self.common == "product.regenerate":
            from apps.product.utils import Regenerate
            objInit = Regenerate
        if self.common == "svn.update":
            from apps.svn_dav.utils import Regenerate
            objInit = Regenerate

        try:
            obj = objInit(debug=0)
            obj.load()
            self.exit_result = obj.finish()
            self.status = 2  # set status "done"
        except Exception, err:
            self.exit_result = traceback.format_exc()
            self.status = 3  # set status "error"
        # --- END RUN --- #

        t2 = datetime.now() - t1
        self.time_long = t2.seconds + t2.microseconds / 1000000.0
        self.save()


class TaskPeriod(models.Model):
    title = models.CharField(max_length=64)
    common = models.CharField(max_length=128)
    date_last = models.DateTimeField(
        _('Date of last generated'), null=True, blank=True)
    is_enable = models.BooleanField(default=False)
    date_start = models.DateTimeField(
        _('Next generating'), default=datetime.now())
    cron = models.CharField(max_length=64, default="*  *  *  *  *")

    def get_previous_run(self):
        if self.date_last:
            return datetime.now() - self.date_last
        return None

    def __unicode__(self):
        return self.title
