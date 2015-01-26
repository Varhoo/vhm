#!/usr/bin/python
# coding: utf-8 
# Author: Pavel Studeník
# Email: studenik@varhoo.cz
# Date: 10.2.2010

from datetime import datetime, timedelta
from django.db import models
from filebrowser.fields import FileBrowseField
from apps.core.models import Account, Domain


class Customer(models.Model):
    name = models.CharField(max_length=200)
    tel = models.CharField(max_length=20)
    email = models.EmailField(max_length=200)

    def __unicode__(self):
        return self.name


class DomainCommmercial(models.Model):
    user = models.ForeignKey(Customer)
    domain = models.ForeignKey(Domain)

    def __unicode__(self):
        return self.domain

    def get_info(self):
        return self.domain.description

    def get_expire(self):
        return self.domain.expire


class Invoice(models.Model):
    user = models.ForeignKey(Customer)
    account = models.ForeignKey(Account)
    date = models.DateField(default=datetime.now)
    month = models.IntegerField(help_text="Number of payed month")
    size = models.IntegerField(help_text="Number of subscieb GB")
    sale = models.IntegerField(help_text="Sleva se zapocita do celkove sumy", default=0)
    price = models.IntegerField(help_text="Celkova suma se slevou", default=0)
    file = FileBrowseField("File", max_length=200, blank=True, null=True)
    is_paid = models.BooleanField(default=False) 

    def date_end(self):
        return (self.date + timedelta(self.month*365/12)).strftime("%d. %m. %Y")

    def __unicode__(self):
        return "%s %s" % (self.account, self.date.isoformat())
