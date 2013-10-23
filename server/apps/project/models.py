from django.db import models
from datetime import datetime
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _


class Project(models.Model):
    owner = models.ForeignKey(User)
    member = models.ManyToManyField(User, related_name="member")
    name = models.CharField(_("name of project"), max_length=128, )
    description = models.TextField(_("description") )
    status = models.CharField(_("status of project"), max_length=128, )
    priority = models.IntegerField(_("priority"), default=1 )
    created = models.DateTimeField(_('created'), default=datetime.now())
    deadline = models.DateTimeField(_('date of deadline'), null=True, blank=True)
    url = models.CharField(_("url of project"), max_length=128, )
 
    def __unicode__(self):
        return self.name

    def get_members(self):
        return self.member.all()
#    @models.permalink
#    def get_absolute_url(self):
#        return ("product_detail" , [self.id,])
      
