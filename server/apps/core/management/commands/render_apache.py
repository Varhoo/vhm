#!/usr/bin/python
# -*- coding: utf-8 -*-

# Author: Pavel Studeník
# Email: studenik@varhoo.cz
# Date: 10.2.2010


from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth.models import User
from django.template.defaultfilters import slugify

from apps.svn_dav.models import *
from apps.auth.models import *
from apps.apftpmy.models import *
from apps.apftpmy.settings import *

import os
import sys
from json import JSONEncoder


class Command(BaseCommand):
    help = ('Get data for render apache\'s sites and director structure')
    requires_model_validation = True
    can_import_settings = True

    def handle(self, *args, **kwargs):
        init(*args, **kwargs)


def init(*args, **kwargs):
    # if repository exist, create .. print SvnRepository.objects.all()

    params = ["apache", "svn"]
    if len(args) != 1 or args[0] not in params:
        print "using: python manage.py render_apache [svn | apache] \n "
        return False

    if params[0] in args:  # param apache
        # render users and passwords
        users = []
        directory = []
        apache_conf = []
        for account in Account.objects.all():
            # get all directories for creating
            path = os.path.normpath(
                "%s%s" % (APACHE_DIR_LOCATION, account.path))
            directory.append(
                {"path": path, "user": slugify(account.name), 'group': APACHE_GROUP})

            # get all users for creating
            users.append(
                {"user": slugify(account.name), 'group': APACHE_GROUP})

            # get all configurations sites
            apache_message = []
            for it in ApacheAlias.objects.filter(account=account.id, is_valid=True):
                if it.site:
                    apache_message.append("# %s" % account.name)
                    apache_message.append("<VirtualHost *:80>")
                    apache_message.append("\tServerName %s" % it.site)
                    apache_message.append("\tDocumentRoot %s/www" % path)
                    # set logs and access information
                    apache_message.append("\tServerSignature On")
                    apache_message.append("\tErrorLog %s/log/error.log" % path)
                    apache_message.append(
                        "\tCustomLog %s/log/access.log combined" % path)
                    apache_message.append("\tLogLevel warn")

                    if it.note:
                        apache_message.append(it.note)

                    for one in AccountAlias.objects.filter(account__id=it.id):
                        apache_message.append("\tServerAlias %s" % one)
                    print it

                    if it.django_wsgi:
                        processname = "%s_%d_%s" % (
                            "wsgi", it.id, account.name)

                        power = APACHE_POWER[it.power]

                        apache_message.append(
                            "\tWSGIScriptAlias / %s/www/.%s.wsgi\n"
                            "\tWSGIDaemonProcess %s user=%s group=%s "
                            "processes=%d threads=%d\n\tWSGIProcessGroup %s" %
                            (path, slugify(it.site), processname, account.name,
                             APACHE_GROUP, power[0], power[1], processname))
                    apache_message.append("</VirtualHost>\n")

                apache_conf.append("\n".join(apache_message))

        data = {"dirs": directory, "users": users, 'apache_site': apache_conf}
        print JSONEncoder().encode(data)

    if params[1] in args:  # param svn
        print "Not implementation"
