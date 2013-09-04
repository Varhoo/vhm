# -*- coding: utf-8 -*-
#Author: Pavel Studeník
#Email: studenik@varhoo.cz
#Date: 10.2.2010

from django.db import models
import settings, random
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
  (0,"None"), 
  (1,"SVN"),
  (2,"GIT"),
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
    hostname = models.SlugField(_("Hostaname"),max_length=64,unique=True)
    description = models.TextField(_("Description"))
    os_type = models.IntegerField(choices=OS_ENUM);
    token = models.CharField(max_length=50,default="".join([random.choice("abcdefghijklmnopqrstuvwxyz0123456789!@#$%^&*(-_=+)") for i in range(50)]))

    def __unicode__(self):
        return "%s" % (self.hostname)

    class META:
        verbose_name = _('Server')
        verbose_name_plurar = _('Servers')

class Account(models.Model):
    owner = models.ForeignKey(User)
    name = models.SlugField(_("Name"),max_length=64,unique=True)
    path = models.CharField(max_length=64, help_text="Určuje cestu k webove prezentaci %s" % settings.APACHE_DIR_LOCATION)
    size = models.IntegerField(_('Size'),default=0)
    token = models.CharField(max_length=50,default="".join([random.choice("abcdefghijklmnopqrstuvwxyz0123456789!@#$%^&*(-_=+)") for i in range(50)]))
    user = models.SlugField()
    uid = models.IntegerField(blank=True,null=True)
    gid = models.IntegerField(blank=True,null=True)
    server = models.ForeignKey(Server)

    def sizeformat(self):
        return filesizeformat(self.size)

    def __unicode__(self):
        return "%s (%s)" % (self.name, self.path)

    class META:
        verbose_name = _('Account')
        verbose_name_plurar = _('Acounts')

class ApacheAlias(models.Model):
    account = models.ForeignKey(Account)
    note = models.TextField(_('Note'), blank=True)
    site = models.CharField(max_length=126)
    django_wsgi = models.BooleanField('Django mode')
    djnago_wsgi_name = models.CharField(max_length=124, null=True, blank=True)
    # svn or git fot update
    repo_type = models.IntegerField(choices=REPOS_ENUM,default=0);
    repo_url = models.CharField(_('Svn update'), max_length=255, null=True, blank=True)
    repo_version = models.CharField(_('Version id/hash'), max_length=128, null=True, blank=True)
    is_valid = models.BooleanField(_('Is valid'))
    comment = models.TextField(_('Comment'), blank=True)
    last_modify = models.DateTimeField(_('Last Modify'), default=datetime.now, blank=True)
    power = models.IntegerField(choices=POWER_ENUM,default=1);

    def __unicode__(self):
        return self.site

class AccountAlias(models.Model):	
    site = models.CharField(max_length=126)
    account = models.ForeignKey(ApacheAlias)

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

class Invoice(models.Model):
    date = models.DateField()
    month = models.IntegerField(help_text="Pocet zaplacenych mesicu služby")
    size = models.IntegerField(help_text="Počet pronajatých GB")
    sale = models.IntegerField(help_text="Sleva se započítá do celkové sumy")
    price = models.IntegerField(help_text="Celková suma se slevou")
    account = models.ForeignKey(Account)
    file = FileBrowseField("File", max_length=200, blank=True, null=True)

    def date_end(self):
        return (self.date + timedelta(self.month*365/12)).strftime("%d. %m. %Y")

    def __unicode__(self):
        return "%s %s" % (self.account, self.date.isoformat())

class Customer(models.Model):
    user = models.ForeignKey(User)
    tel = models.IntegerField(max_length=20)
    email = models.IntegerField(max_length=200)
    invoice = models.ManyToManyField('Invoice')

    def __unicode__(self):
        return self.nazev

