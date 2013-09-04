#!/usr/bin/python
# -*- coding: utf-8 -*-

#Author: Pavel Studeník
#Email: studenik@varhoo.cz
#Date: 10.2.2010

import sys, os, commands, re
from django.core.management import setup_environ
from django.conf import settings as sett

#root path
ROOT_PATH = os.path.dirname(os.path.realpath(__file__))

#load settings from django
sys.path.append(os.path.normpath(ROOT_PATH + "/../../../"))
os.environ['DJANGO_SETTINGS_MODULE'] ='settings.production'
from django.core.management import setup_environ
try:
    import settings  
except:
    msg = "Error: modul settings doesn't load, bad path."
    sys.stderr.write(msg) 
    exit(0)

from apps.apftpmy.models import ApacheAlias

objects = ApacheAlias.objects.filter(repo_url__gt="")
update_count = 0
service_restart = 0

for it in objects:
    homedir = "/var/www/%s/www/" % it.account.path
    command = "cd " + homedir + "; svn diff"
    data = commands.getstatusoutput(command)
    if data[0]==0 and data[1] == "":
        if len(it.repo_version) > 0:
            command = "cd " + homedir + "; svn diff -r BASE:%d; svn update -r %d" % int(it.repo_version)
        else:
            command = "cd " + homedir + "; svn diff -r BASE:HEAD; svn update"
    
        result = commands.getstatusoutput(command)
        if not result[1].startswith("At revision"):
            update_count = update_count + 1 #fix problem revision, reload only when python sripts changes
            print "update projects %s exit code %d" % (it.account, result[0])
            print result[1] 
            command2 = "chown %s:webusers /var/www/%s/www/" %  (it.account.path, it.account.name)
            data = commands.getstatusoutput(command2)
            if len([it for it in result[1].split("\n") if it.endswith(".py")]) > 0:
                # if update python file, need restart apache
                service_restart = service_restart + 1

                #run ./manage.py syncdb - update structure db
                command = "cd " + homedir + "; python manage.py syncdb"
                result = commands.getstatusoutput(command)
                if result[0] != 0:
                    print result

                command = "find " + homedir + " -name '*.pyc' | xargs rm"
                result = commands.getstatusoutput(command)
                if result[0] != 0:
                    print result
    else:
        print "Project %s can't be update" % it.account
        print data[0]
        print "======================="
        print data[1]
        
if service_restart > 0 :
    command = "service apache2 reload" 
    print "[ INFO ] \t Service apache reload ..."
    result = commands.getstatusoutput(command)
    if result[0] > 0:
        print result[1]

