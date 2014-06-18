# -*- coding: utf-8 -*-
#Author: Pavel Studeník
#Email: studenik@varhoo.cz
#Date: 10.2.2010

from django.db import models
import settings, random
import os
from datetime import *
from django.contrib.auth.models import User

from filebrowser.fields import FileBrowseField
from apps.apftpmy.utils import *
from django.template.defaultfilters import filesizeformat
from django.contrib.auth.models import User

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


MODE_ENUM = (
  (0, "None"), 
  (1, "Apache Wsgi"),
  (2, "Apache proxy uWsgi"),
)

OS_ENUM = (
  (0,"Ubuntu/Debian"), 
  (1,"Fedora/CentOS/RHEL"),
)
#i18n
from django.utils.translation import ugettext_lazy as _
# Create your models here.

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
    last_checked = models.DateTimeField(_("last checkdd"), null=True)
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


class Project(models.Model):
    account = models.ForeignKey(Account)
    owner = models.ForeignKey(User)
    site = models.CharField(max_length=126)
    path = models.CharField(max_length=126)
    is_enabled = models.BooleanField(_('Is valid'))
    created = models.DateTimeField(_('Created'), default=datetime.now() )
    last_modify = models.DateTimeField(_('Last Modify'), default=datetime.now(), blank=True)
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


class ProjectProc(models.Model):
    project = models.ForeignKey(ProjectSetting)
    power = models.IntegerField(choices=POWER_ENUM, default=1);
    mode = models.IntegerField('mode', choices=MODE_ENUM)
    mode_params = models.TextField(max_length=256, null=True, blank=True)

    def get_data(self):
        params = [ dict([it.split("=")]) for it in self.mode_params.split(";") if it]
        data = { 
                    "home": self.project.get_path(), 
                    "id": self.id, 
                    "uid": self.project.account.user,
                    "gid": self.project.get_group(),
                    "pythonpath": self.project.account.path,
                    "processes": 1,
                    "optimize": 0,
                    "limit-as": 128,
                    "master": True,
                    "no-orphans": True, 
                    "pidfile": "%s/%d-%s.pid" % (self.project.get_path(), self.id, self.project.account.name),
                    "daemonize": "%s/%d-%s.log" % (self.project.get_path(), self.id, self.project.account.name),
                    "chdir": self.project.account.path,
               }
        for it in params:
            data.update(it)
        if self.mode == 2:
            data["http"] = "%d" % ( self.id + 8000)
            if data.has_key("wsgi-file") and not data["wsgi-file"].startswith("/"):
                data["wsgi-file"] = "%s/%s" % (self.project.get_path(), data["wsgi-file"])
        return data


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


class Customer(models.Model):
    name = models.CharField(max_length=200)
    tel = models.CharField(max_length=20)
    email = models.EmailField(max_length=200)

    def __unicode__(self):
        return self.name


class Invoice(models.Model):
    user = models.ForeignKey(Customer)
    account = models.ForeignKey(Account)
    date = models.DateField(default=datetime.now())
    month = models.IntegerField(help_text="Pocet zaplacenych mesicu služby")
    size = models.IntegerField(help_text="Počet pronajatých GB")
    sale = models.IntegerField(help_text="Sleva se započítá do celkové sumy", default=0)
    price = models.IntegerField(help_text="Celková suma se slevou", default=0)
    file = FileBrowseField("File", max_length=200, blank=True, null=True)
    is_paid = models.BooleanField(default=False) 

    def date_end(self):
        return (self.date + timedelta(self.month*365/12)).strftime("%d. %m. %Y")

    def __unicode__(self):
        return "%s %s" % (self.account, self.date.isoformat())


