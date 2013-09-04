from django.db import models
from filebrowser.fields import FileBrowseField
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _


ENUM_RIGHTS=(
  (1,"Read"),
  (2,"Read and Write"),
);

class SvnRepository(models.Model):
   name = models.SlugField(_("Name repository"),max_length=50,unique=True)

   def users(self):
       return " ,".join([it.user.username for it in SvnUserRights.objects.filter(repository=self.id)])

   def __unicode__(self):
       return "%s" % (self.name)

class SvnGroup(models.Model):
   name = models.SlugField(_("Group of user"),max_length=50,unique=True)

#class SvnGroupRight(models.Model):

class SvnUserRights(models.Model):
   user = models.ForeignKey(User)
   rights = models.IntegerField(_("Rights"),choices=ENUM_RIGHTS,default=1);
   path = models.CharField(_('Path'),max_length=255,default="/") 
   repository = models.ForeignKey(SvnRepository)

   def __unicode__(self):
       return "%s - %s" % (self.repository, self.user.username)
