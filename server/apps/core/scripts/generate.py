#!/usr/bin/python
# -*- coding: utf-8 -*-

#Author: Pavel Studeník
#Email: studenik@varhoo.cz
#Date: 10.2.2010

import sys, os, commands, re
from django.core.management import setup_environ
from django.conf import settings as sett
from django.template.defaultfilters import slugify

set_param_out_dir = None
set_param_no_chown = None

for it in range(len(sys.argv)):
    if sys.argv[it] == "--dir":
        set_param_out_dir = sys.argv[it+1]
    if sys.argv[it] == "--set-chown":
        set_param_no_chown = True
        
#root path
ROOT_PATH = os.path.dirname(os.path.realpath(__file__))

APACHE_CREATE_DIR = True
#load settings from django
sys.path.append(os.path.normpath(ROOT_PATH + "/../../../"))
os.environ['DJANGO_SETTINGS_MODULE'] ='settings.production'
from django.core.management import setup_environ
try:
    import settings  
except:
    msg = "Error:modul settings nebyl nacten, spatna cesta"
    sys.stderr.write(msg) 
    exit(0)


#function create auth for apache and ftpuser
def creatauth(name,homedir):
    """ Function create user in linux for group and set homedir. Function return gid and uid."""

    uid, gid = [None, None]
    #get information about user
    command = "id %s" % (name)
    data = commands.getstatusoutput(command)

    if data[0] > 0:
        #create new system user 
        command = "useradd -g %s %s" % (sett.APACHEIIS_GROUP, name)
        #command = "useradd -g %s %s" % ("www-data",name)
        data = commands.getstatusoutput(command)
        if data[0] != 0:
            msg = "Error: Can't create user."
            sys.stderr.write(msg) 

    #set homedir for user
    command = "usermod -d %s %s" % (homedir,name)
    data = commands.getstatusoutput(command)

    command = "chown %s:%s %s -R" % (name, sett.APACHEIIS_GROUP, homedir)
    data = commands.getstatusoutput(command)

    #get information about user
    command = "id %s" % (name)
    data = commands.getstatusoutput(command)

    #check new user and get uid, gid
    if data[0] > 0:
        msg = "Error: User not create."
        sys.stderr.write(msg) 
    else:
        for it in data[1].split(" "):
            m = re.search('uid=([0-9]*)', it)
            try:
                uid = m.group(1)
            except:
                pass

            m = re.search('gid=([0-9]*)', it)
            try:
                gid = m.group(1)
            except:
                pass

        return {"uid":uid,"gid":gid}
    return {}


setup_environ(settings)

#get admin information
admin = [item for item in settings.ADMINS][0]

from apps.apftpmy.models import *
from apps.apftpmy.settings import *
#from apacheiis.apache.settings import *

#get all objects for apache2
data = Account.objects.all()

#generování site-avaible/default pro apache
#apache_message.append("ServerAdmin %s" % (admin[1]))
for item in data:
    path = os.path.normpath("%s%s" % (APACHE_DIR_LOCATION,item.path))
    try:
        if APACHE_CREATE_DIR:
            #create dir
            if not os.path.exists(path):
                os.mkdir(path)
    except:
        msg = "Warning: dir '%s' not create\n" % (path)
        sys.stderr.write(msg) 

    #apache lines for render settings
    apache_message = []
    for it in ApacheAlias.objects.filter(account=item.id, is_valid=True):
        if not it.site:
            continue
        apache_message.append("# %s" % item.name)
        apache_message.append("<VirtualHost *:80>")
        apache_message.append("\tServerName %s" % it.site)
        apache_message.append("\tDocumentRoot %s/www" % path)
        #set logs and access information
        apache_message.append("\tServerSignature On")
        apache_message.append("\tErrorLog %s/log/error.log" % path)
        apache_message.append("\tCustomLog %s/log/access.log combined" % path)
        apache_message.append("\tLogLevel warn")
        if not os.path.exists("%s/log/" % path):
            os.mkdir("%s/log/" % path)
        if not os.path.exists("%s/www/" % path):
            os.mkdir("%s/www/" % path)
            
        if it.note: 
            apache_message.append(it.note)

        for one in AccountAlias.objects.filter(account__id=it.id):
            apache_message.append("\tServerAlias %s" % one)

        if it.django_wsgi:
            processname = "%s_%d_%s" % ("wsgi",it.id, item.name)
            #FIXME set number of prosses and thread from db
            power = [1,2]
            if it.power == 2:
                power = [2,4]
            else:
                if it.power == 3: 
                    power = [3,6]
                else:
                    power = [1,2]
            apache_message.append(
                "\tWSGIScriptAlias / %s/www/.%s.wsgi\n"
                "\tWSGIDaemonProcess %s user=%s group=%s "
                "processes=%d threads=%d\n\tWSGIProcessGroup %s" % 
                ( path, slugify(it.site), processname, item.name,
                  sett.APACHEIIS_GROUP, power[0], power[1], processname) )
        else:
            # set user and group for apache mod
            apache_message.append( "AssignUserId %s %s" % (item.name, sett.APACHEIIS_GROUP) )

        apache_message.append("</VirtualHost>\n")

    if len(apache_message)>0:
        if set_param_out_dir:
            fw = open("%s/%03d-%s" %(set_param_out_dir,item.id,item.name) ,'w')
            fw.write("\n".join(apache_message))
            fw.close()
        else:
            print "\n".join(apache_message)
    
        if set_param_no_chown:
            #create system user
            osid = creatauth(item.name, path)
            #FIXME update db
            #save gid and uid
            for it in Ftpuser.objects.filter(account__id=item.id):
                if it.uid != osid["uid"] or it.gid != osid["gid"]:
                    it.uid = osid["uid"]
                    it.gid = osid["gid"]
                    it.save()

    #update size of dir
    command = "du -sb %s | awk '{print $1}'" % (path)
    try:
        data = commands.getstatusoutput(command)
        item.size = data[1]
        item.save()
    except:
        pass

