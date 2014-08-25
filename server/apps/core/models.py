# -*- coding: utf-8 -*-
#Author: Pavel Studeník
#Email: studenik@varhoo.cz
#Date: 10.2.2010

import settings, random
import os
from datetime import *
from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _
from django.template.defaultfilters import filesizeformat
from django.contrib.auth.models import User
from django.template import Context
from django.template import Template

from utils import *



POWER_ENUM = (
  (1, "Low"), 
  (2, "Medium"),
  (3, "Hight"),
)

REPOS_ENUM = (
  (0, "None"), 
  (1, "SVN"),
  (2, "GIT"),
)

MODE_ENUM_APACHE = 1
MODE_ENUM_VHM = 2
MODE_ENUM = (
  (MODE_ENUM_APACHE, "Apache"),
  (MODE_ENUM_VHM, "VHM-manager"),
)

OS_ENUM = (
  (0, "Ubuntu/Debian"), 
  (1, "Fedora/CentOS/RHEL"),
)


class Domain(models.Model):
    owner = models.ForeignKey(User)
    name = models.CharField(_("Domain name"), max_length=128, )
    expirate = models.DateField(_('Expirate'), blank=True, null=True, default=datetime.now)
    description = models.TextField(_("Description"), blank=True)
    last_modify = models.DateTimeField(_('Last Modify'),null=True,blank=True)

    def check_pay(self):
        days = diff_date_days(self.expirate, datetime.now())
        return "%s days" % days

    def __unicode__(self):
        return self.name

    class META:
        verbose_name = _('Domain')
        verbose_name_plurar = _('Domains')


class Server(models.Model):
    hostname = models.CharField(_("Hostaname"), max_length=64, unique=True)
    description = models.TextField(_("Description"))
    total_mem = models.IntegerField(_("Total Memory"), default=0)
    total_hd = models.IntegerField(_("Total Disk"), default=0)
    last_checked = models.DateTimeField(_("last checkdd"), null=True, blank=True)
    global_ip = models.IPAddressField(default="0.0.0.0")
    os_type = models.IntegerField(choices=OS_ENUM);
    token = models.CharField(max_length=50,default="".join([random.choice("abcdefghijklmnopqrstuvwxyz0123456789!@#$%^&*(-_=+)") for i in range(50)]))

    def __unicode__(self):
        return "%s" % (self.hostname)

    class META:
        verbose_name = _('Server')
        verbose_name_plurar = _('Servers')


class Account(models.Model):
    owner = models.ForeignKey(User)
    server = models.ForeignKey(Server)
    name = models.SlugField(_("Name"), max_length=64,unique=True)
    path = models.CharField(max_length=64, help_text="Určuje cestu k webove prezentaci %s" % settings.APACHE_DIR_LOCATION, default=settings.APACHE_DIR_LOCATION)
    size = models.IntegerField(_('Size'), default=0)
    token = models.CharField(max_length=50,default="".join([random.choice("abcdefghijklmnopqrstuvwxyz0123456789!@#$%^&*(-_=+)") for i in range(50)]))
    user = models.SlugField()
    uid = models.IntegerField(blank=True, null=True)
    gid = models.IntegerField(blank=True, null=True)

    def sizeformat(self):
        return filesizeformat(self.size)

    def __unicode__(self):
        return "%s (%s)" % (self.name, self.path)

    class META:
        verbose_name = _('Account')
        verbose_name_plurar = _('Acounts')

    def save(self, *args, **kwargs):
        if not self.id:
            pass
        else:
            pass
        super(Account, self).save(*args, **kwargs)


class Project(models.Model):
    account = models.ForeignKey(Account)
    owner = models.ForeignKey(User)
    site = models.CharField(max_length=126)
    path = models.CharField(max_length=126)
    is_enabled = models.BooleanField(_('Is valid'))
    created = models.DateTimeField(_('Created'), default=datetime.now )
    last_modify = models.DateTimeField(_('Last Modify'), default=datetime.now, blank=True)
    note = models.TextField(_('Note'), blank=True)

    def get_path(self):
        return os.path.abspath("%s/%s" % (self.account.path, self.path ))

    def get_group(self):
        return settings.APACHE_GROUP

    def __unicode__(self):
        return self.site


class ProjectSetting(Project):
    repo_type = models.IntegerField(choices=REPOS_ENUM, default=0);
    repo_url = models.CharField(_('Repo update'), max_length=256, null=True, blank=True)
    repo_version = models.CharField(_('Version id/hash'), max_length=128, null=True, blank=True)
    comment = models.TextField(_('Comment'), blank=True)
    last_update = models.DateTimeField(_('Last Update'), null=True, blank=True)


class TemplateProc(models.Model):
    title = models.CharField(max_length=256)
    file_type = models.IntegerField(choices=MODE_ENUM)
    content = models.TextField()
    comment = models.TextField(blank=True)
    last_update = models.DateTimeField(_('Last Update'), default=datetime.now)

    def __unicode__(self):
        return "%s" % self.title


class ProjectProc(models.Model):
    project = models.ForeignKey(ProjectSetting)
    template = models.ForeignKey(TemplateProc)
    params = models.TextField(max_length=256, null=True, blank=True)
    is_running = models.BooleanField(_('Is running'), default=False)

    def is_enabled(self):
        return self.project.is_enabled
    is_enabled.boolean = True

    def get_account(self):
        return self.project.account

    def get_data(self):
        params = [ dict([it.split("=")]) for it in self.mode_params.split(";") if it]
        data = { 
                    "home": self.project.get_path(), 
                    "id": self.id, 
                    "uid": self.project.account.user,
                    "gid": self.project.get_group(),
                    "pythonpath": self.project.get_path(),
                    "processes": 1,
                    "optimize": 0,
                    "limit-as": 128,
                    "master": True,
                    "no-orphans": True, 
                    "pidfile": os.path.abspath("%s/%d-%s.pid" % \
                           (self.project.account.path, self.id, \
                            self.project.account.name)),
                    "daemonize":  os.path.abspath("%s/log/%d-%s.log" % \
                           (self.project.account.path, self.id, \
                            self.project.account.name)),
                    "chdir": self.project.get_path(),
               }
        for it in params:
            data.update(it)
        if self.mode == 2:
            data["socket"] = "%s:%d" % ("0.0.0.0", self.id + 8000)
            if data.has_key("wsgi-file") and not data["wsgi-file"].startswith("/"):
                data["wsgi-file"] = "%s/%s" % (self.project.get_path(), data["wsgi-file"])
        return data

    def get_template(self):
        return self.template.content

    def get_raw(self):
        project = self.project
        account = self.project.account
        alias_list = [it.site for it in DomainAlias.objects.filter(project=project)]
        data = {
            "id": self.id,
            "name": project.account.name,
            "root": self.project.account.path,
            "root_proc": project.get_path(),
            "admin_email": account.owner.email,
            "domain": project.site,
            "alias_list": alias_list,
            "uid": project.account.user,
            "gid": project.get_group(),
            "port": "%d" % (8000 + self.id),
        }
        c = Context(data)
        t = Template(self.template.content)
        #print t.render(c)
        return t.render(c)


class DomainAlias(models.Model):	
    site = models.CharField(max_length=126)
    project = models.ForeignKey(Project)

    def __unicode__(self):
        return self.site


class Ftpuser(models.Model):
#userid 	passwd 	uid 	gid 	homedir 	shell 	count 	accessed 	modified
    account = models.ForeignKey(Account)
    userid = models.CharField(max_length=50,unique=True)
    passwd = models.CharField(max_length=50)
    uid = models.IntegerField()
    gid = models.IntegerField()
    homedir = models.CharField(max_length=150,default="/var/www/")
    shell = models.CharField(max_length=50,default="/bin/false")

    def __unicode__(self):
    	return self.userid
    class Meta:
        db_table = "ftpusers"


